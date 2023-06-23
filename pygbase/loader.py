from typing import Type, Callable

import pygame

from .game_state import GameState
from .resources import ResourceManager


class Loading(GameState, name="loading"):
	def __init__(self, after_load_state: Type[GameState], run_on_load_complete: tuple[Callable, ...]):  # noqa
		# From GameState, but no parent __init__ call, so have to do it manually
		self.id = -1
		self._next_state = self

		ResourceManager.init_load()

		self.after_load_state = after_load_state
		self.run_on_load_complete = run_on_load_complete

	def update(self, delta: float):
		if ResourceManager.load_update():  # Done loading
			for func in self.run_on_load_complete:
				func()

			self.set_next_state(self.after_load_state())

	def draw(self, surface: pygame.Surface):
		surface.fill((0, 0, 0))
