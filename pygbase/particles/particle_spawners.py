import random
from abc import abstractmethod

import pygame

from ..common import Common
from ..particles.particle_manager import ParticleManager
from ..timer import Timer
from ..utils import get_angled_vector


class ParticleSpawner:
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: str, manager: ParticleManager):
		self.active = start_active

		self.pos = pygame.Vector2(pos)

		self.timer = Timer(cooldown, True, True)
		self.amount = amount

		self.type = particle_type
		self.manager = manager

		self.particle_settings = Common.get_particle_setting(particle_type)

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
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: str, manager: ParticleManager):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

	def spawn(self):
		self.manager.add_particle(
			self.pos,
			self.particle_settings,
			get_angled_vector(random.uniform(0.0, 360.0), random.uniform(100.0, 200.0))
		)


class CircleSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, radius: float, start_active: bool, particle_type: str, manager: ParticleManager):
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
			self.particle_settings
		)


class RectSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, size: tuple, start_active: bool, particle_type: str, manager: ParticleManager):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

		self.size = size

	def spawn(self):
		spawn_offset = random.uniform(0, self.size[0]), random.uniform(0, self.size[1])

		self.manager.add_particle(
			self.pos + spawn_offset,
			self.particle_settings
		)
