from typing import TypeVar, TYPE_CHECKING

import pygame

from .particle_affectors import AffectorTypes, ParticleAttractor
from ..camera import Camera
from ..debug import DebugDisplay
from ..particles.particle import Particle

if TYPE_CHECKING:
	from .particle_spawners import ParticleSpawner

	SpawnerType = TypeVar("SpawnerType", bound=ParticleSpawner)
	AffectorType = TypeVar("AffectorType", bound=ParticleAttractor)


# TODO: Add way to clear all particles
class ParticleManager:
	def __init__(self, chunk_size: int = 400):
		self.chunk_size = chunk_size

		self.particles: dict[int, dict[int, list[Particle]]] = {}

		self.spawners: list[ParticleSpawner] = []

		self.affectors: dict[AffectorTypes, list[ParticleAttractor]] = {
			AffectorTypes.ATTRACTOR: []
		}

	def add_particle(self, pos: tuple | pygame.Vector2, settings: dict, initial_velocity=(0, 0)):
		chunk_col, chunk_row = self.get_chunk(pos)

		self.particles.setdefault(
			chunk_row, {}
		).setdefault(
			chunk_col, []
		).append(Particle(pos, settings, initial_velocity))

	def get_particles(self, pos: tuple | pygame.Vector2, size: tuple | pygame.Vector2) -> list[Particle]:
		left_chunk_col, top_chunk_row = self.get_chunk(pos)
		right_chunk_col, bottom_chunk_row, = self.get_chunk(pos + size)

		return [
			particle
			for row in range(top_chunk_row, bottom_chunk_row + 1)
			for col in range(left_chunk_col, right_chunk_col + 1)
			for particle in self.particles.get(row, {}).get(col, [])
		]

	def get_chunk(self, pos: tuple | pygame.Vector2):
		return int(pos[0] // self.chunk_size), int(pos[1] // self.chunk_size)

	def add_spawner(self, spawner: "SpawnerType") -> "SpawnerType":
		self.spawners.append(spawner)
		return spawner

	def remove_spawner(self, spawner: "SpawnerType"):
		if spawner in self.spawners:
			self.spawners.remove(spawner)

	def add_affector(self, affector_type: AffectorTypes, affector: "AffectorType") -> "AffectorType":
		self.affectors[affector_type].append(affector)
		return affector

	def update(self, delta: float):
		for spawner in self.spawners:
			spawner.update(delta)

		for affector_type, affectors in self.affectors.items():
			for affector in affectors:
				affector.affect_particles(
					delta,
					self.get_particles(
						affector.pos - pygame.Vector2(affector.radius)
						, pygame.Vector2(affector.radius) * 2
					)
				)

		particles_to_move: list[Particle] = []
		chunks_to_delete: list[tuple[int, int]] = []
		for row, chunk_row in self.particles.items():
			for col, chunk in chunk_row.items():
				for particle in chunk:
					particle.update(delta)

					new_chunk_col, new_chunk_row = self.get_chunk(particle.pos)

					if new_chunk_col != col or new_chunk_row != row:
						particles_to_move.append(particle)
						particle.moved_chunk()

				chunk[:] = [particle for particle in chunk if particle.alive()]
				if len(chunk) == 0:
					chunks_to_delete.append((col, row))

		for chunk in chunks_to_delete:
			del self.particles[chunk[1]][chunk[0]]

		for particle in particles_to_move:
			chunk_col, chunk_row = self.get_chunk(particle.pos)

			self.particles.setdefault(
				chunk_row, {}
			).setdefault(
				chunk_col, []
			).append(particle)
			particle.has_moved_chunk = False

	def draw(self, surface: pygame.Surface, camera: Camera):
		[
			particle.draw(surface, camera)
			for row in self.particles.values()
			for chunk in row.values()
			for particle in chunk
		]

		# Debug
		if DebugDisplay.is_active():
			for row in self.particles.keys():
				for col in self.particles[row].keys():
					DebugDisplay.draw_rect(pygame.Rect(
						camera.world_to_screen((col * self.chunk_size, row * self.chunk_size)),
						(self.chunk_size, self.chunk_size)
					), "blue", width=2)

			for affector_type, affectors in self.affectors.items():
				for affector in affectors:
					left_chunk_col, top_chunk_row = self.get_chunk(affector.pos - pygame.Vector2(affector.radius))
					right_chunk_col, bottom_chunk_row, = self.get_chunk((affector.pos - pygame.Vector2(affector.radius)) + pygame.Vector2(affector.radius) * 2)

					for row in range(top_chunk_row, bottom_chunk_row + 1):
						for col in range(left_chunk_col, right_chunk_col + 1):
							DebugDisplay.draw_circle(camera.world_to_screen(affector.pos), affector.radius, "yellow")

							DebugDisplay.draw_rect(pygame.Rect(
								camera.world_to_screen((col * self.chunk_size, row * self.chunk_size)),
								(self.chunk_size, self.chunk_size)
							), "yellow")
