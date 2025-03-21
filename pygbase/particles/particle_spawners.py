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
	def __init__(self, pos: pygame.typing.Point, cooldown: float, amount: int, start_active: bool, particle_type: str, manager: "ParticleManager"):
		self._linked_pos: bool
		if isinstance(pos, pygame.Vector2):
			self._linked_pos = True
			self.pos = pos
		else:
			self._linked_pos = False
			self.pos = pygame.Vector2(pos)

		self.timer = Timer(cooldown, True, True)
		self.amount = amount

		self.type = particle_type
		self.manager = manager

		self.particle_settings = Common.get_particle_setting(particle_type)

		self.active = start_active

	def update_pos(self, pos):
		if self._linked_pos:
			raise RuntimeError("Cannot modify linked position")

		self.pos.update(pos)

	@abstractmethod
	def spawn(self):
		pass

	def update(self, delta: float):
		"""Will run when active"""

		self.timer.tick(delta)

		if self.timer.done():
			for _ in range(self.amount):
				self.spawn()


class PointSpawner(ParticleSpawner):
	def __init__(self, pos, cooldown: float, amount: int, start_active: bool, particle_type: str, manager: "ParticleManager", angle_range: tuple[float, float] = (0, 360), velocity_range: tuple[float, float] = (100.0, 200.0)):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

		self.angle_range = angle_range
		self.velocity_range = velocity_range

	def spawn(self):
		initial_velocity = get_angled_vector(random.uniform(*self.angle_range), random.uniform(*self.velocity_range))

		self.manager.add_particle(
			self.pos,
			self.particle_settings,
			initial_velocity
		)


class CircleSpawner(ParticleSpawner):
	def __init__(
			self,
			pos: pygame.typing.Point,
			cooldown: float,
			amount: int,
			radius: float,
			start_active: bool,
			particle_type: str,
			manager: "ParticleManager",
			spawn_velocity: pygame.typing.Point = (0, 0),
			linear_velocity_range: tuple[tuple[float, float], tuple[float, float]] = ((0, 0), (0, 0)),
			radial_velocity_range: tuple[float, float] = (0, 0),
			radial_offset_range: tuple[float, float] = (0, 0)
	):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)
		self.radius = radius

		self.spawn_velocity = pygame.Vector2(spawn_velocity)
		self.linear_velocity_range = linear_velocity_range
		self.radial_velocity_range = radial_velocity_range
		self.radial_offset_range = radial_offset_range

	def spawn(self):
		offset = get_angled_vector(random.uniform(0, 360), random.uniform(0, self.radius ** 2) ** 0.5)
		offset.rotate_ip_rad(random.uniform(*self.radial_offset_range))

		self.manager.add_particle(
			self.pos + offset,
			self.particle_settings,
			initial_velocity=(
					offset.normalize()
					* random.uniform(*self.radial_velocity_range)
					+ pygame.Vector2(random.uniform(*self.linear_velocity_range[0]), random.uniform(*self.linear_velocity_range[1]))
					+ self.spawn_velocity
			)

		)


class RectSpawner(ParticleSpawner):
	def __init__(self, pos: pygame.typing.Point, cooldown: float, amount: int, size: tuple, start_active: bool, particle_type: str, manager: "ParticleManager"):
		super().__init__(pos, cooldown, amount, start_active, particle_type, manager)

		self.size = size

	def spawn(self):
		spawn_offset = random.uniform(0, self.size[0]), random.uniform(0, self.size[1])

		self.manager.add_particle(
			self.pos + spawn_offset,
			self.particle_settings
		)
