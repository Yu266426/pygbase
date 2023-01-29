from typing import Callable, Any

import pygame

from .game_state import GameStateIds


class EventManager:
	handlers: dict[int, dict[int, list[Callable[[pygame.event.Event], None]]]] = {}

	@classmethod
	def init(cls):
		for game_state in GameStateIds:
			cls.handlers[game_state] = {}

	@classmethod
	def add_handler(cls, game_state: int, event_type: int, handler: Callable[[pygame.event.Event], None]):
		if event_type not in cls.handlers:
			cls.handlers[game_state][event_type] = []

		cls.handlers[game_state][event_type].append(handler)

	@classmethod
	def handle_events(cls, current_game_state: int):
		for event in pygame.event.get():
			if event.type in cls.handlers[current_game_state]:
				for handler in cls.handlers[current_game_state][event.type]:
					handler(event)
			elif event.type in cls.handlers[GameStateIds.ALL]:
				for handler in cls.handlers[GameStateIds.ALL][event.type]:
					handler(event)

	@classmethod
	def run_handlers(cls, game_state: int, event_type: int, **kwargs):
		for handler in cls.handlers[game_state][event_type]:
			handler(pygame.event.Event(event_type, kwargs))

	@classmethod
	def post_event(cls, event_type: int, **kwargs: dict[str, Any]):
		pygame.event.post(pygame.event.Event(event_type, kwargs))
