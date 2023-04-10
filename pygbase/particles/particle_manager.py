import pygame

from ..particles.particle import Particle
from ..particles.particle_settings import ParticleTypes


class ParticleManager:
	def __init__(self):
		self.particles = []

		self.spawners = []

		self.affectors: dict[str, list] = {
			"attractor": []
		}

	def add_particle(self, pos, particle_type: ParticleTypes, initial_velocity=(0, 0)):
		self.particles.append(Particle(pos, particle_type, initial_velocity))

	def add_spawner(self, spawner):
		self.spawners.append(spawner)
		return spawner

	def add_affector(self, affector_type, affector):
		self.affectors[affector_type].append(affector)
		return affector

	def update(self, delta: float):
		for spawner in self.spawners:
			spawner.update(delta)

		for particle in self.particles[:]:
			particle.update(delta, self.affectors)

			if not particle.alive():
				self.particles.remove(particle)

	def draw(self, screen: pygame.Surface, scroll: pygame.Vector2):
		for particle in self.particles:
			particle.draw(screen, scroll)
