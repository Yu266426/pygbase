import pygame

import pygbase
from .light import Light
from .lighting_manager import LightingManager


def init_lighting(max_radius: int, interval: int):
	pygbase.Common.set_value("max_light_radius", max_radius)
	pygbase.Common.set_value("light_radius_interval", interval)

	generate_lights(max_radius, interval)


def generate_lights(max_radius: int, interval: int, power: float = 1.4):
	lights = Light.cached_lights

	max_light_surf = pygame.Surface((max_radius * 2, max_radius * 2), flags=pygame.SRCALPHA)
	for inner in range(max_radius, 0, -1):
		factor = 1 - (inner / max_radius) ** power
		colour = int(255 * factor)

		pygame.draw.circle(max_light_surf, (colour, colour, colour, colour), (max_radius, max_radius), inner)

	lights.append(max_light_surf)

	reference_surface = max_light_surf
	for radius in range(max_radius - 1, 0, -interval):
		new_light_surface = pygame.transform.smoothscale(reference_surface, (radius * 2, radius * 2))
		lights.append(new_light_surface)

		if radius <= int((reference_surface.get_width() * 0.75) / 2):
			# print(radius)
			reference_surface = new_light_surface

	lights.reverse()

	# for index, light_surf in enumerate(lights):
	# 	pygame.image.save(light_surf, f"/Users/tigerz/Documents/Programming/Github/pygbase/temp/light_{index}.png")
	#
	# print(len(lights))
	# print(lights[0], lights[max_light_radius - 1])
	pass
