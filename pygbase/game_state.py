from typing import Type

import pygame

from .common import Common


class GameState:
	child_state_id = 1

	def __init_subclass__(cls, **kwargs):
		if "name" not in kwargs:
			raise KeyError("\"name\" keyword argument not in class definition. It should look like <class Child(GameState, name=\"child\")>")

		name = kwargs["name"]

		# Disregard built in game_states
		if (
				name == "loading" or
				name == "transition" or
				name == "fade_transition"
		):
			return

		# Add id to common and child class, then increment by 1
		Common.add_game_state(name, GameState.child_state_id)
		cls.id = GameState.child_state_id

		GameState.child_state_id += 1

	def __init__(self):
		self._next_state = self

	def enter(self):
		"""Called when entering state"""
		pass

	def exit(self):
		"""Called when exiting state"""
		pass

	def set_next_state(self, next_state: "GameState"):
		self._next_state = next_state

	def set_next_state_type(self, next_state: Type["GameState"], args: tuple):
		if len(args) > 0:
			self._next_state = next_state(*args)
		else:
			self._next_state = next_state()

	def get_next_state(self) -> "GameState":
		return self._next_state

	def update(self, delta: float):
		pass

	def fixed_update(self, delta: float):
		pass

	def draw(self, surface: pygame.Surface):
		pass
