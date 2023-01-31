from abc import abstractmethod

import pygame


class GameState:
	def __init__(self, state_id: int):
		if state_id == 0:
			raise ValueError(f"The id 0 is reserved by pygbase for every game state")
		elif state_id == 1:
			raise ValueError(f"The id 1 is reserved by pygbase for the resource loader")

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
