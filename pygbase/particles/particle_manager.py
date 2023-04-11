import pygame

from .particle_affectors import AffectorTypes
from ..camera import Camera
from ..particles.particle import Particle


class ParticleManager:
	def __init__(self):
		self.particles = []

		self.spawners = []

		self.affectors: dict[AffectorTypes, list] = {
			AffectorTypes.ATTRACTOR: []
		}

	def add_particle(self, pos, settings: dict, initial_velocity=(0, 0)):
		self.particles.append(Particle(pos, settings, initial_velocity))

	def add_spawner(self, spawner):
		self.spawners.append(spawner)
		return spawner

	def add_affector(self, affector_type: AffectorTypes, affector):
		self.affectors[affector_type].append(affector)
		return affector

	def update(self, delta: float):
		[spawner.update(delta) for spawner in self.spawners]
		[particle.update(delta, self.affectors) for particle in self.particles]
		self.particles[:] = [particle for particle in self.particles if particle.alive()]

	def draw(self, screen: pygame.Surface, camera: Camera):
		[particle.draw(screen, camera) for particle in self.particles]
