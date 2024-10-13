import pygame

from .light import Light
from ..camera import Camera
from ..common import Common


class LightingManager:
	def __init__(self, default_brightness: float):
		self.brightness = default_brightness
		self.lighting_surf = pygame.Surface((Common.get_value("screen_width"), Common.get_value("screen_height")))
		self.lighting_surf.fill((int(255 * default_brightness), int(255 * default_brightness), int(255 * default_brightness)))

		self.add_lighting_surf = pygame.Surface((Common.get_value("screen_width"), Common.get_value("screen_height")), flags=pygame.SRCALPHA)
		self.add_lighting_surf.fill((0, 0, 0))

		self.lights: list[Light] = []

	def add_light(self, light_source: Light) -> Light:
		self.lights.append(light_source)
		return light_source

	def remove_light(self, light_source: Light):
		if light_source in self.lights:
			self.lights.remove(light_source)

	def update(self, delta):
		for light in self.lights:
			light.update(delta)

	def draw(self, surface: pygame.Surface, camera: Camera):
		lighting_surf = self.lighting_surf.copy()
		add_lighting_surf = self.add_lighting_surf.copy()

		for light in self.lights:
			light.draw(lighting_surf, add_lighting_surf, camera)

		surface.blit(lighting_surf, (0, 0), special_flags=pygame.BLEND_MULT)
		surface.blit(add_lighting_surf, (0, 0), special_flags=pygame.BLEND_ADD)
