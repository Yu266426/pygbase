from abc import abstractmethod
from typing import Type

import pygame


class GameState:
	def __init__(self, state_id: int):
		if state_id == 0:
			raise ValueError(f"The id 0 is reserved by pygbase for every game state")

		self.id: int = state_id

		self._next_state = self

	def set_next_state(self, next_state: Type["GameState"], *args):
		if len(args) == 0:
			self._next_state = next_state()  # NoQA
		else:
			self._next_state = next_state(args)  # NoQA

	def next_state(self) -> "GameState":
		return self._next_state

	@abstractmethod
	def update(self, delta: float):
		pass

	@abstractmethod
	def draw(self, screen: pygame.Surface):
		pass
