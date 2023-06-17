import math

import pygame

from ..camera import Camera


class Light:
	def __init__(self, pos, brightness, radius, variation, variation_speed, linked_pos=True, camera_affected=True):
		self.start_time = pygame.time.get_ticks() / 1000

		self.pos = pos if linked_pos else pygame.Vector2(pos)

		self.brightness = brightness
		self.radius = radius

		self.variation = variation
		self.variation_speed = variation_speed

		self.surface = pygame.Surface(((self.radius + self.variation) * 2, (self.radius + self.variation) * 2), flags=pygame.SRCALPHA)

		self.camera_affected = camera_affected

	def update(self, delta):
		pass

	def draw(self, surface: pygame.Surface, camera: Camera):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		colour = max(0, min(255, 255 * self.brightness + variation / 20))
		self.surface.fill((0, 0, 0))
		pygame.draw.circle(self.surface, (colour, colour, colour), (self.radius, self.radius), self.radius + variation)

		if self.camera_affected:
			surface.blit(self.surface, self.surface.get_rect(center=camera.world_to_screen(self.pos)), special_flags=pygame.BLEND_ADD)
		else:
			surface.blit(self.surface, self.surface.get_rect(center=self.pos), special_flags=pygame.BLEND_ADD)
