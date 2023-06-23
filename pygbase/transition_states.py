import pygame

from . import Common
from .game_state import GameState


class Transition(GameState, name="transition"):
	def __init__(self, current_state: GameState, to_state: GameState):  # NoQA
		self.id = -2
		self._next_state = self

		self.current_state = current_state
		self.to_state = to_state

	def update(self, delta: float):
		pass

	def draw(self, surface: pygame.Surface):
		pass


class FadeTransition(Transition, name="fade_transition"):
	def __init__(self, current_state: GameState, to_state: GameState, transition_time: float, fade_colour: tuple[int, int, int]):
		super().__init__(current_state, to_state)

		self.transition_time = transition_time

		self.fade_colour = fade_colour

		self.fade_amount = 0
		self.fade_in = True

		self.fade_surface = pygame.Surface(
			(Common.get_value("screen_width"), Common.get_value("screen_height")),
			flags=pygame.SRCALPHA
		)

	def update(self, delta: float):
		self.fade_surface.fill((*self.fade_colour, self.fade_amount))

		if self.fade_in:
			self.fade_amount += 255 / (self.transition_time / 2) * delta
			if self.fade_amount >= 255:
				self.fade_amount = 255
				self.fade_in = False

			self.current_state.update(delta)
		else:
			self.fade_amount -= 255 / (self.transition_time / 2) * delta
			if self.fade_amount <= 0:
				self.set_next_state(self.to_state)

			self.to_state.update(delta)

	def draw(self, surface: pygame.Surface):
		if self.fade_in:
			self.current_state.draw(surface)
		else:
			self.to_state.draw(surface)
		surface.blit(self.fade_surface, (0, 0))
