import random

import pygame

from ..camera import Camera
from ..common import ParticleOptions as Options


class Particle:
	def __init__(self, pos: tuple | pygame.Vector2, settings: dict, initial_velocity=(0, 0)):
		self.pos = pygame.Vector2(pos)

		self.size: float = random.uniform(
			settings[Options.SIZE][0],
			settings[Options.SIZE][1]
		)
		self.size_decay: float = random.uniform(
			settings[Options.SIZE_DECAY][0],
			settings[Options.SIZE_DECAY][1]
		)

		self.colour = random.choice(settings[Options.COLOUR])

		self.velocity: pygame.Vector2 = pygame.Vector2(initial_velocity)
		self.velocity_decay: float = random.uniform(
			settings[Options.VELOCITY_DECAY][0],
			settings[Options.VELOCITY_DECAY][1]
		)

		self.gravity: tuple = settings[Options.GRAVITY]
		self.effector: bool = settings[Options.EFFECTOR]

		self.bounce: tuple = settings[Options.BOUNCE]

		self.has_moved_chunk = False

	def moved_chunk(self):
		self.has_moved_chunk = True

	def alive(self):
		return self.size > 0.2 and not self.has_moved_chunk

	def update(self, delta: float, colliders: list[pygame.Rect]):
		self.velocity.x += self.gravity[0]
		self.velocity.x -= self.velocity.x * delta * self.velocity_decay

		self.pos.x += self.velocity.x * delta

		for collider in colliders:
			if collider.collidepoint(self.pos):
				self.pos.x -= self.velocity.x * delta
				self.velocity.x *= -self.bounce[0]

		self.velocity.y += self.gravity[1]
		self.velocity.y -= self.velocity.y * delta * self.velocity_decay

		self.pos.y += self.velocity.y * delta

		for collider in colliders:
			if collider.collidepoint(self.pos):
				self.pos.y -= self.velocity.y * delta
				self.velocity.y *= -self.bounce[1]

		self.size -= delta * self.size_decay

	def draw(self, screen: pygame.Surface, camera: Camera):
		pygame.draw.rect(screen, self.colour, (camera.world_to_screen(self.pos - pygame.Vector2(round(self.size / 2))), (self.size, self.size)))
