import abc
from abc import abstractmethod

import pygame.math


class Tween(abc.ABC):
	def __init__(self, values: tuple[float, ...], time: float):
		self._time = time
		self._progress = 0

		if len(values) < 2:
			raise ValueError("Must have at least two values for tween")

		self._values = values
		self._num_values = len(values)

	@abstractmethod
	def value(self) -> float:
		pass

	def _get_current_next_progress_values(self) -> tuple[float, float, float]:
		current_index = int(self._progress * (self._num_values - 1))

		if current_index >= self._num_values - 1:
			return self._values[-1], 0, 0

		next_index = current_index + 1
		progress_to_next = self._progress % (1 / (self._num_values - 1)) * (self._num_values - 1)

		current_value = self._values[current_index]
		next_value = self._values[next_index]

		return current_value, next_value, progress_to_next

	def set_progress(self, value: float):
		self._progress = pygame.math.clamp(value, 0.0, 1.0)

	def tick(self, delta: float):
		self.set_progress(self._progress + delta / self._time)


class LinearTween(Tween):
	def __init__(self, values: tuple[float, ...], time: float):
		super().__init__(values, time)

	def value(self) -> float:
		current_value, next_value, progress_to_next = self._get_current_next_progress_values()
		return current_value + (next_value - current_value) * progress_to_next


class CubicTween(Tween):
	def __init__(self, values: tuple[float, ...], time: float):
		super().__init__(values, time)

	@staticmethod
	def _cubic_ease(progress) -> float:
		if progress < 0.5:
			return 4 * (progress ** 3)
		else:
			return 1 - pow(-2 * progress + 2, 3) / 2

	def value(self) -> float:
		current_value, next_value, progress_to_next = self._get_current_next_progress_values()
		return current_value + (next_value - current_value) * self._cubic_ease(progress_to_next)
