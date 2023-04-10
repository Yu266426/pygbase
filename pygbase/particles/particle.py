import random

import pygame

from .. import Common
from ..particles.particle_affectors import ParticleAttractor
from ..particles.particle_settings import ParticleTypes
from ..particles.particle_settings import ParticleOptions as Options


class Particle:
	def __init__(self, pos, particle_type: ParticleTypes, initial_velocity=(0, 0)):
		settings = Common.get_value("particle_settings")

		self.pos = pygame.Vector2(pos)

		self.size = random.uniform(
			settings[particle_type][Options.SIZE][0],
			settings[particle_type][Options.SIZE][1]
		)
		self.size_decay = random.uniform(
			settings[particle_type][Options.SIZE_DECAY][0],
			settings[particle_type][Options.SIZE_DECAY][1]
		)

		self.colour = settings[particle_type][Options.COLOUR]

		self.velocity = pygame.Vector2(initial_velocity)
		self.velocity_decay = random.uniform(
			settings[particle_type][Options.VELOCITY_DECAY][0],
			settings[particle_type][Options.VELOCITY_DECAY][1]
		)

		self.gravity = settings[particle_type][Options.GRAVITY]
		self.effector = settings[particle_type][Options.EFFECTOR]

	def alive(self):
		return self.size > 0.2

	def update(self, delta, affectors: dict[str, list]):
		if self.effector:
			for attractor in affectors["attractor"]:
				attractor: ParticleAttractor

				direction_vector, distance = attractor.get_towards(self.pos)
				if distance < 6:
					self.size = 0
					return

				self.velocity += direction_vector * attractor.strength * min(attractor.strength * 40 / distance, 10)

		self.velocity += self.gravity
		self.velocity -= self.velocity * delta * self.velocity_decay

		self.pos += self.velocity * delta

		self.size -= delta * self.size_decay

	def draw(self, screen: pygame.Surface, scroll: pygame.Vector2):
		pygame.draw.rect(screen, self.colour, (self.pos - scroll, (self.size, self.size)))
