import random
from abc import abstractmethod

import pygame

from ..particles.particle_manager import ParticleManager
from ..particles.particle_settings import ParticleTypes
from ..timer import Timer
from ..utils import get_angled_vector


class ParticleSpawner:
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: ParticleTypes, manager: ParticleManager):
		self.active = start_active

		self.pos = pygame.Vector2(pos)

		self.timer = Timer(cooldown, True, True)
		self.amount = amount

		self.type = particle_type
		self.manager = manager

	def link_pos(self, pos: pygame.Vector2) -> "ParticleSpawner":
		self.pos = pos
		return self

	def update_pos(self, new_pos):
		self.pos.update(new_pos)

	@abstractmethod
	def spawn(self):
		pass

	def update(self, delta: float):
		if self.active:
			self.timer.tick(delta)

			if self.timer.done():
				for _ in range(self.amount):
					self.spawn()


class PointSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: ParticleTypes, manager: ParticleManager):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

	def spawn(self):
		self.manager.add_particle(self.pos, ParticleTypes.DEFAULT, get_angled_vector(random.uniform(0.0, 360.0), random.uniform(100.0, 200.0)))


class CircleSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, radius: float, start_active: bool, particle_type: ParticleTypes, manager: ParticleManager):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)
		self.pos = pygame.Vector2(pos)
		self.radius = radius

		self.timer = Timer(cooldown, True, True)
		self.amount = amount

		self.type = particle_type

		self.manager = manager

	def spawn(self):
		self.manager.add_particle(
			self.pos + get_angled_vector(random.uniform(0, 360), random.uniform(0, self.radius)),
			self.type
		)
