import random

import pygame

from ..camera import Camera
from ..particles.particle_affectors import ParticleAttractor, AffectorTypes
from ..particles.particle_settings import ParticleOptions as Options


class Particle:
	def __init__(self, pos, settings: dict, initial_velocity=(0, 0)):
		self.pos = pygame.Vector2(pos)

		self.size = random.uniform(
			settings[Options.SIZE][0],
			settings[Options.SIZE][1]
		)
		self.size_decay = random.uniform(
			settings[Options.SIZE_DECAY][0],
			settings[Options.SIZE_DECAY][1]
		)

		self.colour = random.choice(settings[Options.COLOUR])

		self.velocity = pygame.Vector2(initial_velocity)
		self.velocity_decay = random.uniform(
			settings[Options.VELOCITY_DECAY][0],
			settings[Options.VELOCITY_DECAY][1]
		)

		self.gravity = settings[Options.GRAVITY]
		self.effector = settings[Options.EFFECTOR]

	def alive(self):
		return self.size > 0.2

	def update(self, delta, affectors: dict[AffectorTypes, list]):
		if self.effector:
			for attractor in affectors[AffectorTypes.ATTRACTOR]:
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

	def draw(self, screen: pygame.Surface, camera: Camera):
		pygame.draw.rect(screen, self.colour, (camera.world_to_screen(self.pos), (self.size, self.size)))
