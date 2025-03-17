import enum
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
	from .particle import Particle


class AffectorTypes(enum.Enum):
	ATTRACTOR = enum.auto()


class ParticleAttractor:
	def __init__(self, pos: pygame.typing.Point, radius: float, strength: float):
		self._linked_pos: bool
		if isinstance(pos, pygame.Vector2):
			self._linked_pos = True
			self.pos = pos
		else:
			self._linked_pos = False
			self.pos = pygame.Vector2(pos)

		self.radius = radius
		self.strength = strength

		self.active = True

	def update_pos(self, pos):
		if self._linked_pos:
			raise RuntimeError("Cannot modify linked position")

		self.pos.update(pos)

	def _get_towards(self, pos: pygame.Vector2) -> tuple[pygame.Vector2, float]:
		direction_vector = self.pos - pos
		return direction_vector.normalize(), direction_vector.length()

	def affect_particles(self, delta: float, particles: list["Particle"]):
		"""Will run when active"""

		for particle in particles:
			if particle.effector:
				direction_vector, distance = self._get_towards(particle.pos)

				if distance > self.radius:
					continue

				if distance < 6:
					particle.size = 0
					continue

				particle.velocity += direction_vector * (self.strength / distance) * delta
