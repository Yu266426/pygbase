import pygame

import pygbase
from .light import Light
from .lighting_manager import LightingManager
from .shadow import Shadow

__all__ = ["Light", "LightingManager", "Shadow"]


def init_lighting_system(
	max_light_radius: int, max_shadow_radius: int, interval: int, shadow_ratio: float
):
	pygbase.Common.set("max_light_radius", max_light_radius)
	pygbase.Common.set("lighting_radius_interval", interval)
	pygbase.Common.set("shadow_ratio", shadow_ratio)

	generate_lights(max_light_radius, interval)
	generate_shadows(max_shadow_radius, interval, shadow_ratio)


def generate_lights(max_radius: int, interval: int, power: float = 1.4):
	lights = Light.cached_lights

	# Create largest light surface
	max_light_surf = pygame.Surface((max_radius * 2, max_radius * 2), flags=pygame.SRCALPHA)
	for inner in range(max_radius, 0, -1):
		factor = 1 - (inner / max_radius) ** power
		colour = int(255 * factor)

		pygame.draw.circle(
			max_light_surf, (colour, colour, colour, colour), (max_radius, max_radius), inner
		)

	lights.append(max_light_surf)

	# Generate the rest based on max (and shrink the reference every so often for performance)
	reference_surface = max_light_surf
	for radius in range(max_radius - 1, 0, -interval):
		new_light_surf = pygame.transform.smoothscale(reference_surface, (radius * 2, radius * 2))
		lights.append(new_light_surf)

		if radius <= int((reference_surface.get_width() * 0.75) / 2):
			reference_surface = new_light_surf

	lights.reverse()


def generate_shadows(max_radius: int, interval: int, shadow_ratio: float, power: float = 3):
	shadows = Shadow.cached_shadows

	# Create the largest shadow surface
	max_shadow_surf = pygame.Surface((max_radius * 2, max_radius * 2), flags=pygame.SRCALPHA)
	for inner in range(max_radius, 0, -1):
		factor = 1 - (inner / max_radius) ** power
		colour = int(255 * factor)

		pygame.draw.circle(
			max_shadow_surf, (colour, colour, colour, colour), (max_radius, max_radius), inner
		)

	shadows.append(
		pygame.transform.smoothscale(
			max_shadow_surf, (2 * max_radius * shadow_ratio, 2 * max_radius / shadow_ratio)
		)
	)

	# Generate the rest based on max (and shrink the reference every so often for performance)
	reference_surface = max_shadow_surf
	for radius in range(max_radius - 1, 0, -interval):
		new_shadow_surf = pygame.transform.smoothscale(reference_surface, (radius * 2, radius * 2))
		shadows.append(
			pygame.transform.smoothscale(
				new_shadow_surf, (2 * radius * shadow_ratio, 2 * radius / shadow_ratio)
			)
		)

		if radius <= int((reference_surface.get_width() * 0.75) / 2):
			reference_surface = new_shadow_surf

	shadows.reverse()
