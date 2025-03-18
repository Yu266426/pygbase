import math

import pygame

from ..camera import Camera
from ..common import Common


class Light:
	cached_lights: list[pygame.Surface] = []

	def __init__(
			self,
			pos: pygame.typing.Point,
			brightness: float,
			radius: float,
			variation: float,
			variation_speed: float,
			camera_affected: bool = True,
			tint=(255, 255, 255),
	):
		self.start_time = pygame.time.get_ticks() / 1000

		self._linked_pos: bool
		if isinstance(pos, pygame.Vector2):
			self._linked_pos = True
			self.pos = pos
		else:
			self._linked_pos = False
			self.pos = pygame.Vector2(pos)

		self.brightness = pygame.math.clamp(brightness, 0, 1)
		self.add_brightness = pygame.math.clamp(brightness - 1, 0, 1)

		self.radius = radius
		self.variation = variation
		self.variation_speed = variation_speed

		self.brightness_surface = pygame.Surface(
			((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA
		)
		self.brightness_surface.fill(
			(int(255 * self.brightness), int(255 * self.brightness), int(255 * self.brightness))
		)

		if self.add_brightness > 0:
			self.add_brightness_surface = pygame.Surface(
				((self.radius + self.variation) * 2, (self.radius + self.variation) * 2),
				flags=pygame.SRCALPHA,
			)
			self.add_brightness_surface.fill(
				(
					int(255 * self.add_brightness),
					int(255 * self.add_brightness),
					int(255 * self.add_brightness),
				)
			)

		self.tint = tint
		self.tint_surface = pygame.Surface(
			((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA
		)
		self.tint_surface.fill(self.tint)

		self.camera_affected = camera_affected

		self.radius_interval = Common.get("lighting_radius_interval")

	def update_pos(self, pos):
		if self._linked_pos:
			raise RuntimeError("Cannot modify linked position")

		self.pos.update(pos)

	def set_brightness(self, brightness: float):
		self.brightness = pygame.math.clamp(brightness, 0, 1)
		self.add_brightness = pygame.math.clamp(brightness - 1, 0, 1)

		self.brightness_surface.fill(
			(int(255 * self.brightness), int(255 * self.brightness), int(255 * self.brightness))
		)

		if self.add_brightness > 0:
			self.add_brightness_surface.fill(
				(
					int(255 * self.add_brightness),
					int(255 * self.add_brightness),
					int(255 * self.add_brightness),
				)
			)

	def update(self, delta):
		pass

	def draw(self, surface: pygame.Surface, add_surface: pygame.Surface, camera: Camera):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		radius = int(self.radius + variation)
		# colour = int(max(0.0, min(1.0, self.brightness + variation / 20)))

		light_surface = self.cached_lights[int(radius / self.radius_interval) - 1].copy()

		light_surface.blit(self.brightness_surface, (0, 0), special_flags=pygame.BLEND_MULT)
		light_surface.blit(self.tint_surface, (0, 0), special_flags=pygame.BLEND_MULT)

		if self.add_brightness > 0:
			add_light_surface = self.cached_lights[int(radius / self.radius_interval) - 1].copy()

			add_light_surface.blit(self.add_brightness_surface, (0, 0), special_flags=pygame.BLEND_MULT)
			add_light_surface.blit(self.tint_surface, (0, 0), special_flags=pygame.BLEND_MULT)

		if self.camera_affected:
			surface.blit(
				light_surface,
				light_surface.get_rect(center=camera.world_to_screen(self.pos)),
				special_flags=pygame.BLEND_ADD,
			)

			if self.add_brightness > 0:
				add_surface.blit(
					add_light_surface,
					add_light_surface.get_rect(center=camera.world_to_screen(self.pos)),
					special_flags=pygame.BLEND_ADD,
				)

		else:
			surface.blit(
				light_surface, light_surface.get_rect(center=self.pos), special_flags=pygame.BLEND_ADD
			)

			if self.add_brightness > 0:
				add_surface.blit(
					add_light_surface,
					add_light_surface.get_rect(center=self.pos),
					special_flags=pygame.BLEND_ADD,
				)
