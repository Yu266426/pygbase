import pygame

import pygbase
from .light import Light
from .lighting_manager import LightingManager


def init(max_light_radius: int = 600):
	pygbase.Common.set_value("max_light_radius", max_light_radius)

	generate_lights(max_light_radius)


def generate_lights(max_light_radius: int):
	lights = Light.cached_lights

	max_light_surf = pygame.Surface((max_light_radius * 2, max_light_radius * 2), flags=pygame.SRCALPHA)
	for inner in range(max_light_radius, 0, -1):
		factor = 1 - (inner / max_light_radius) ** 1.5
		colour = int(255 * factor)

		pygame.draw.circle(max_light_surf, (colour, colour, colour), (max_light_radius, max_light_radius), inner)

	for radius in range(max_light_radius):
		lights.append(pygame.transform.smoothscale(max_light_surf, (radius * 2, radius * 2)))
