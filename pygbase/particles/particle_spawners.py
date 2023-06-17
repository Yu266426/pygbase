import random
from abc import abstractmethod
from typing import TYPE_CHECKING

import pygame

from ..common import Common
from ..timer import Timer
from ..utils import get_angled_vector

if TYPE_CHECKING:
	from ..particles.particle_manager import ParticleManager


class ParticleSpawner:
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: str, manager: "ParticleManager"):
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
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: str, manager: "ParticleManager"):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

	def spawn(self):
		self.manager.add_particle(
			self.pos,
			self.particle_settings,
			get_angled_vector(random.uniform(0.0, 360.0), random.uniform(100.0, 200.0))
		)


class CircleSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, radius: float, start_active: bool, particle_type: str, manager: "ParticleManager", linear_velocity_range: tuple[tuple[float, float], tuple[float, float]] = ((0, 0), (0, 0)), radial_velocity_range: tuple[float, float] = (0, 0)):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)
		self.pos = pygame.Vector2(pos)
		self.radius = radius

		self.timer = Timer(cooldown, True, True)
		self.amount = amount

		self.type = particle_type

		self.manager = manager

		self.linear_velocity_range = linear_velocity_range
		self.radial_velocity_range = radial_velocity_range

	def spawn(self):
		offset = get_angled_vector(random.uniform(0, 360), random.uniform(0, self.radius ** 2) ** 0.5)
		self.manager.add_particle(
			self.pos + offset,
			self.particle_settings,
			initial_velocity=offset.normalize() * random.uniform(*self.radial_velocity_range) + pygame.Vector2(random.uniform(*self.linear_velocity_range[0]), random.uniform(*self.linear_velocity_range[1]))
		)


class RectSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, size: tuple, start_active: bool, particle_type: str, manager: "ParticleManager"):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

		self.size = size

	def spawn(self):
		spawn_offset = random.uniform(0, self.size[0]), random.uniform(0, self.size[1])

		self.manager.add_particle(
			self.pos + spawn_offset,
			self.particle_settings
		)
