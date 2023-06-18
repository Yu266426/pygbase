import math

import pygame

import pygbase
from ..camera import Camera


class Light:
	cached_lights: list[pygame.Surface] = []

	def __init__(self, pos: pygame.Vector2 | tuple[float, float], brightness: float, radius: float, variation: float, variation_speed: float, camera_affected: bool = True, tint=(255, 255, 255)):
		self.start_time = pygame.time.get_ticks() / 1000

		self.pos = pos

		self.brightness = brightness

		self.radius = radius
		self.variation = variation
		self.variation_speed = variation_speed

		self.brightness_surface = pygame.Surface(((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA)
		self.brightness_surface.fill((int(255 * self.brightness), int(255 * self.brightness), int(255 * self.brightness)))

		self.tint = tint
		self.tint_surface = pygame.Surface(((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA)
		self.tint_surface.fill(self.tint)

		self.camera_affected = camera_affected

		self.radius_interval = pygbase.Common.get_value("light_radius_interval")

	def link_pos(self, pos: pygame.Vector2) -> "Light":
		self.pos = pos
		return self

	def update(self, delta):
		pass

	def draw(self, surface: pygame.Surface, camera: Camera):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		radius = int(self.radius + variation)
		# colour = int(max(0.0, min(1.0, self.brightness + variation / 20)))

		light_surface = self.cached_lights[int(radius / self.radius_interval) - 1].copy()

		light_surface.blit(self.brightness_surface, (0, 0), special_flags=pygame.BLEND_MULT)
		light_surface.blit(self.tint_surface, (0, 0), special_flags=pygame.BLEND_MULT)

		if self.camera_affected:
			surface.blit(light_surface, light_surface.get_rect(center=camera.world_to_screen(self.pos)), special_flags=pygame.BLEND_ADD)
		else:
			surface.blit(light_surface, light_surface.get_rect(center=self.pos), special_flags=pygame.BLEND_ADD)
