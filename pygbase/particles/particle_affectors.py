import enum
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
	from particles.particle import Particle


class AffectorTypes(enum.Enum):
	ATTRACTOR = enum.auto()


class ParticleAttractor:
	def __init__(self, pos: tuple | pygame.Vector2, radius: float, strength: float):
		self.pos = pygame.Vector2(pos)
		self.radius = radius
		self.strength = strength

	def update_pos(self, new_pos):
		self.pos.update(new_pos)

	def link_pos(self, pos: pygame.Vector2) -> "ParticleAttractor":
		self.pos = pos
		return self

	def get_towards(self, pos: pygame.Vector2) -> tuple[pygame.Vector2, float]:
		direction_vector = self.pos - pos
		return direction_vector.normalize(), direction_vector.length()

	def affect_particles(self, delta: float, particles: list["Particle"]):
		for particle in particles:
			if particle.effector:
				direction_vector, distance = self.get_towards(particle.pos)

				if distance > self.radius:
					continue

				if distance < 6:
					particle.size = 0
					continue

				particle.velocity += direction_vector * (self.strength / distance) * delta
