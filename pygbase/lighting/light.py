import math

import pygame

from ..camera import Camera


class Light:
	def __init__(self, pos: pygame.Vector2 | tuple[float, float], brightness: float, radius: float, variation: float, variation_speed: float, camera_affected: bool = True, tint=(255, 255, 255)):
		self.start_time = pygame.time.get_ticks() / 1000

		self.pos = pos

		self.brightness = brightness

		self.radius = radius
		self.variation = variation
		self.variation_speed = variation_speed

		self.surface = pygame.Surface(((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA)
		self.surface_center = self.surface.get_rect().center

		self.tint = tint
		self.tint_surface = pygame.Surface(((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA)
		self.tint_surface.fill(self.tint)

		self.camera_affected = camera_affected

	def link_pos(self, pos: pygame.Vector2) -> "Light":
		self.pos = pos
		return self

	def update(self, delta):
		pass

	def draw(self, surface: pygame.Surface, camera: Camera):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		colour = int(max(0.0, min(255.0, 255 * self.brightness + variation / 20)))
		self.surface.fill((0, 0, 0))
		pygame.draw.circle(self.surface, (colour, colour, colour), self.surface_center, self.radius + variation)
		self.surface.blit(self.tint_surface, (0, 0), special_flags=pygame.BLEND_MULT)

		if self.camera_affected:
			surface.blit(self.surface, self.surface.get_rect(center=camera.world_to_screen(self.pos)), special_flags=pygame.BLEND_ADD)
		else:
			surface.blit(self.surface, self.surface.get_rect(center=self.pos), special_flags=pygame.BLEND_ADD)
