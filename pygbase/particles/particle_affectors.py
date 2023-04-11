import enum

import pygame


class AffectorTypes(enum.Enum):
	ATTRACTOR = enum.auto()


class ParticleAttractor:
	def __init__(self, pos=(0, 0), strength=1):
		self.pos = pygame.Vector2(pos)
		self.strength = strength

	def update_pos(self, new_pos):
		self.pos.update(new_pos)

	def link_pos(self, pos: pygame.Vector2) -> "ParticleAttractor":
		self.pos = pos
		return self

	def get_towards(self, pos: pygame.Vector2) -> tuple[pygame.Vector2, float]:
		direction_vector = self.pos - pos
		return direction_vector.normalize(), direction_vector.length()
