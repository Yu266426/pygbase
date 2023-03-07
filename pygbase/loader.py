from typing import Type, Union

import pygame

from .resources import ResourceManager
from .game_state import GameState


class Loading(GameState):
	def __init__(self, after_load_state: Type[GameState]):  # noqa
		# From GameState, but no parent __init__ call, so have to do it manually
		self.id = -1
		self._next_state = self

		ResourceManager.init_load()

		self.after_load_state = after_load_state

	def update(self, delta: float):
		if ResourceManager.load_update():
			self.set_next_state(self.after_load_state)

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))
