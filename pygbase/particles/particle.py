import random

import pygame

from ..camera import Camera
from ..particles.particle_affectors import ParticleAttractor, AffectorTypes
from ..common import ParticleOptions as Options


class Particle:
	def __init__(self, pos: tuple | pygame.Vector2, settings: dict, initial_velocity=(0, 0)):
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

		self.has_moved_chunk = False

	def moved_chunk(self):
		self.has_moved_chunk = True

	def alive(self):
		return self.size > 0.2 and not self.has_moved_chunk

	def update(self, delta):
		self.velocity += self.gravity
		self.velocity -= self.velocity * delta * self.velocity_decay

		self.pos += self.velocity * delta

		self.size -= delta * self.size_decay

	def draw(self, screen: pygame.Surface, camera: Camera):
		pygame.draw.rect(screen, self.colour, (camera.world_to_screen(self.pos - pygame.Vector2(round(self.size / 2))), (self.size, self.size)))
