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


class ParticleManager:
	def __init__(self, chunk_size: int = 400, colliders: tuple[pygame.Rect] = ()):
		self.chunk_size = chunk_size

		self.particles: dict[tuple[int, int], list[Particle]] = {}

		self.spawners: list[ParticleSpawner] = []

		self.affectors: dict[AffectorTypes, list[ParticleAttractor]] = {
			AffectorTypes.ATTRACTOR: []
		}

		self.chunked_colliders: dict[tuple[int, int], list[pygame.Rect]] = {}
		self.generate_chunked_colliders(colliders)
		self.dynamic_colliders: list[pygame.Rect] = []

	def generate_chunked_colliders(self, colliders):
		chunked_colliders = {}

		for collider in colliders:
			for x in range(collider.left, collider.right, self.chunk_size):
				for y in range(collider.top, collider.bottom, self.chunk_size):
					chunk_pos = self.get_chunk((x, y))

					chunked_colliders.setdefault(
						chunk_pos, []
					).append(collider)

		self.chunked_colliders = chunked_colliders

	def pass_dynamic_colliders(self, colliders: list[pygame.Rect]):
		self.dynamic_colliders[:] = colliders[:]  # Contents of dynamic_colliders gets set to contents of colliders

	def get_surrounding_colliders(self, chunk_pos: tuple):
		min_row = chunk_pos[1] - 1
		max_row = chunk_pos[1] + 2
		min_col = chunk_pos[0] - 1
		max_col = chunk_pos[0] + 2

		colliders = []
		for row in range(min_row, max_row):
			for col in range(min_col, max_col):
				colliders.extend(self.chunked_colliders.get((col, row), []))

		return colliders

	def add_particle(self, pos: tuple | pygame.Vector2, settings: dict, initial_velocity=(0, 0)):
		chunk_pos = self.get_chunk(pos)

		self.particles.setdefault(
			chunk_pos, []
		).append(Particle(pos, settings, initial_velocity))

	def get_particles(self, pos: tuple | pygame.Vector2, size: tuple | pygame.Vector2) -> list[Particle]:
		# TODO: Optimize in same way as `get_surrounding_colliders`
		left_chunk_col, top_chunk_row = self.get_chunk(pos)
		right_chunk_col, bottom_chunk_row, = self.get_chunk(pos + size)

		return [
			particle
			for row in range(top_chunk_row, bottom_chunk_row + 1)
			for col in range(left_chunk_col, right_chunk_col + 1)
			for particle in self.particles.get((col, row), [])
		]

	def clear(self):
		for chunk_pos, chunk in self.particles.items():
			chunk.clear()

		self.particles.clear()

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
						affector.pos - pygame.Vector2(affector.radius),
						pygame.Vector2(affector.radius) * 2
					)
				)

		particles_to_move: list[Particle] = []
		chunks_to_delete: list[tuple[int, int]] = []
		for chunk_pos, chunk in self.particles.items():
			surrounding_colliders = [*self.get_surrounding_colliders(chunk_pos), *self.dynamic_colliders]

			for particle in chunk:
				particle.update(delta, surrounding_colliders)

				new_chunk_pos = self.get_chunk(particle.pos)

				if new_chunk_pos != chunk_pos:
					particles_to_move.append(particle)
					particle.moved_chunk()

			chunk[:] = [particle for particle in chunk if particle.alive()]
			if len(chunk) == 0:
				chunks_to_delete.append(chunk_pos)

		for chunk_pos in chunks_to_delete:
			del self.particles[chunk_pos]

		for particle in particles_to_move:
			chunk_pos = self.get_chunk(particle.pos)

			self.particles.setdefault(
				chunk_pos, []
			).append(particle)
			particle.has_moved_chunk = False

	def draw(self, surface: pygame.Surface, camera: Camera):
		[
			particle.draw(surface, camera)
			for chunk in self.particles.values()
			for particle in chunk
		]

		# Debug
		if DebugDisplay.is_active():
			for (col, row) in self.particles.keys():
				DebugDisplay.draw_rect(pygame.Rect(
					camera.world_to_screen((col * self.chunk_size, row * self.chunk_size)),
					(self.chunk_size, self.chunk_size)
				), "blue", width=2)

			for chunk in self.chunked_colliders.values():
				for collider in chunk:
					DebugDisplay.draw_rect(pygame.Rect(
						camera.world_to_screen(collider.topleft),
						collider.size
					), "light blue", width=3)

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
