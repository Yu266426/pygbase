import enum
from abc import abstractmethod

import pygame


class GameStateIds(enum.IntEnum):
	ALL = 0
	LOADING = 1
	MAIN_MENU = 2
	GAME = 3
	EDITOR = 4


class GameState:
	def __init__(self, state_id: int):
		self.id: int = state_id

	@abstractmethod
	def next_state(self) -> "GameState":
		pass

	@abstractmethod
	def update(self, delta: float):
		pass

	@abstractmethod
	def draw(self, screen: pygame.Surface):
		pass
