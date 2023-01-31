from typing import Type, Union

import pygame

from .resources import ResourceManager
from .game_state import GameState


class Loading:
	def __init__(self, after_load_state: Type[GameState]):
		self.id = 1

		ResourceManager.init_load()

		self.should_switch = False
		self.after_load_state = after_load_state

	def next_state(self) -> Union["Loading", GameState]:
		if self.should_switch:
			return self.after_load_state()
		return self

	def update(self, delta: float):
		self.should_switch = ResourceManager.load_update()

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))
