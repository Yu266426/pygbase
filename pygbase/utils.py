import math

import pygame


def get_angled_vector(angle: float, magnitude: float):
	return pygame.Vector2(1, 0).rotate(angle) * magnitude


def get_angle_to(pos: tuple[int | float, int | float] | pygame.Vector2, to: tuple[int | float, int | float] | pygame.Vector2) -> float:
	# Gets the relative angle
	return math.degrees(math.atan2(pos[1] - to[1], to[0] - pos[0]))
