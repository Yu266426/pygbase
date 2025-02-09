import logging
import math
import random

import pygame
from pygame import Surface

from ..camera import Camera
from ..common import ParticleOptions as Options, Common


class Particle:
	__slots__ = [
		"pos",
		"size",
		"size_decay",
		"color",
		"velocity",
		"velocity_decay",
		"gravity",
		"effector",
		"bounce_ranges",
		"cache",
		"has_moved_chunk",
	]

	PARTICLE_IMAGE_CACHE: dict[str, dict[pygame.typing.ColorLike, list[pygame.Surface]]] = {}

	@classmethod
	def cache_particle_images(cls):
		logging.debug("Caching Particles")

		for particle_type, particle_data in Common.get_particle_settings().items():
			cache = {}

			colors = particle_data[Options.COLOR]
			largest_size = particle_data[Options.SIZE][1]

			for color in colors:
				cache[color] = []
				for size in range(0, math.ceil(largest_size)):
					surface = pygame.Surface((size, size))
					surface.fill(color)
					cache[color].append(surface)

			cls.PARTICLE_IMAGE_CACHE[particle_type] = cache

	def __init__(self, pos: pygame.typing.Point, settings: dict, initial_velocity=(0, 0)):
		self.pos = pygame.Vector2(pos)

		self.size: float = random.uniform(settings[Options.SIZE][0], settings[Options.SIZE][1])
		self.size_decay: float = random.uniform(
			settings[Options.SIZE_DECAY][0], settings[Options.SIZE_DECAY][1]
		)

		self.color = random.choice(settings[Options.COLOR])

		self.velocity: pygame.Vector2 = pygame.Vector2(initial_velocity)
		self.velocity_decay: float = random.uniform(
			settings[Options.VELOCITY_DECAY][0], settings[Options.VELOCITY_DECAY][1]
		)

		self.gravity: tuple = settings[Options.GRAVITY]
		self.effector: bool = settings[Options.EFFECTOR]

		self.bounce_ranges: tuple[tuple, tuple] = settings[Options.BOUNCE]

		self.cache = self.PARTICLE_IMAGE_CACHE[settings[Options.NAME]][self.color]

		self.has_moved_chunk = False

	def moved_chunk(self):
		self.has_moved_chunk = True

	def alive(self):
		return self.size > 0.2 and not self.has_moved_chunk

	def update(self, delta: float, colliders: list[pygame.Rect | pygame.FRect]):
		# Pre-calculate some repeated values
		gravity_x = self.gravity[0] * delta
		gravity_y = self.gravity[1] * delta
		decay = delta * self.velocity_decay
		size_decay = delta * self.size_decay

		# Update x velocity
		vel_x = self.velocity.x
		vel_x += gravity_x
		vel_x -= vel_x * decay

		new_pos_x = self.pos.x + vel_x * delta

		for collider in colliders:
			if collider.collidepoint(new_pos_x, self.pos.y):
				new_pos_x -= vel_x * delta
				vel_x *= -random.uniform(*self.bounce_ranges[0])
				break  # TODO: Potentially buggy

		# Update y velocity
		vel_y = self.velocity.y
		vel_y += gravity_y
		vel_y -= vel_y * decay

		new_pos_y = self.pos.y + vel_y * delta

		# Check collisions and handle bounces
		for collider in colliders:
			if collider.collidepoint(new_pos_x, new_pos_y):
				new_pos_y -= vel_y * delta
				vel_y *= -random.uniform(*self.bounce_ranges[1])
				break

		# Update position and velocity
		self.pos.x = new_pos_x
		self.pos.y = new_pos_y
		self.velocity.x = vel_x
		self.velocity.y = vel_y

		# Update size
		self.size -= size_decay

	def get_blit_pair(self, camera: Camera) -> tuple[Surface, tuple[int, int]]:
		return self.cache[int(self.size)], camera.world_to_screen(self.pos - pygame.Vector2(round(self.size / 2)))
