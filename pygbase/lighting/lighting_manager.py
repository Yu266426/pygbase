import logging

import pygame

from .light import Light
from .shadow import Shadow
from ..camera import Camera
from ..common import Common


class LightingManager:
	def __init__(self, default_brightness: float, shadow_brightness: float):
		self.brightness = default_brightness
		self.shadow_brightness = shadow_brightness

		self.lighting_surf = pygame.Surface((Common.get_value("screen_width"), Common.get_value("screen_height")))
		self.lighting_surf.fill((int(255 * default_brightness), int(255 * default_brightness), int(255 * default_brightness)))

		self.add_lighting_surf = pygame.Surface((Common.get_value("screen_width"), Common.get_value("screen_height")), flags=pygame.SRCALPHA)
		self.add_lighting_surf.fill((0, 0, 0))

		self.shadow_surf = pygame.Surface((Common.get_value("screen_width"), Common.get_value("screen_height")))
		self.shadow_surf.fill((255, 255, 255))

		self.lights: list[Light] = []
		self.shadows: list[Shadow] = []

	def add_light(self, light_source: Light) -> Light:
		self.lights.append(light_source)
		return light_source

	def remove_light(self, light_source: Light):
		if light_source in self.lights:
			self.lights.remove(light_source)

	def add_shadow(self, shadow: Shadow) -> Shadow:
		shadow.init_surf(int(self.shadow_brightness * 255))
		self.shadows.append(shadow)
		return shadow

	def remove_shadow(self, shadow: Shadow):
		if shadow in self.shadows:
			self.shadows.remove(shadow)

	def update(self, delta):
		for light in self.lights:
			light.update(delta)

	def draw_shadows(self, surface: pygame.Surface, camera: Camera):
		shadow_surf = self.shadow_surf.copy()

		for shadow in self.shadows:
			shadow.draw(shadow_surf, camera)

		surface.blit(shadow_surf, (0, 0), special_flags=pygame.BLEND_MULT)

	def draw_lights(self, surface: pygame.Surface, camera: Camera):
		lighting_surf = self.lighting_surf.copy()
		add_lighting_surf = self.add_lighting_surf.copy()

		for light in self.lights:
			light.draw(lighting_surf, add_lighting_surf, camera)

		surface.blit(lighting_surf, (0, 0), special_flags=pygame.BLEND_MULT)
		surface.blit(add_lighting_surf, (0, 0), special_flags=pygame.BLEND_ADD)
