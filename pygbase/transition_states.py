import pygame

from .game_state import GameState


class Transition(GameState):
	def __init__(self, current_state: GameState, to_state: GameState):  # noqa
		self.id = -2
		self._next_state = self

		self.current_state = current_state
		self.to_state = to_state

		raise NotImplementedError("Transitions are in development")

	def update(self, delta: float):
		pass

	def draw(self, screen: pygame.Surface):
		pass


class FadeTransition(Transition):
	def __init__(self, current_state: GameState, to_state: GameState, transition_time: float):
		super().__init__(current_state, to_state)

		self.transition_time = transition_time

	def next_state(self) -> GameState:
		return self

	def update(self, delta: float):
		pass

	def draw(self, screen: pygame.Surface):
		pass
