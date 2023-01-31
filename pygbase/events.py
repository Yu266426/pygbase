from typing import Callable, Any

import pygame


class EventManager:
	handlers: dict[int, dict[int, list[Callable[[pygame.event.Event], None]]]] = {}

	@classmethod
	def init(cls):
		# 0 is base state
		cls.handlers[0] = {}

	@classmethod
	def add_handler(cls, game_state: int, event_type: int, handler: Callable[[pygame.event.Event], None]):
		if game_state not in cls.handlers:
			cls.handlers[game_state] = {}

		if event_type not in cls.handlers[game_state]:
			cls.handlers[game_state][event_type] = []

		cls.handlers[game_state][event_type].append(handler)

	@classmethod
	def handle_events(cls, current_game_state: int):
		for event in pygame.event.get():
			if current_game_state in cls.handlers:
				if event.type in cls.handlers[current_game_state]:
					for handler in cls.handlers[current_game_state][event.type]:
						handler(event)

					break

			if event.type in cls.handlers[0]:
				for handler in cls.handlers[0][event.type]:
					handler(event)

	@classmethod
	def run_handlers(cls, game_state: int, event_type: int, **kwargs):
		for handler in cls.handlers[game_state][event_type]:
			handler(pygame.event.Event(event_type, kwargs))

	@classmethod
	def post_event(cls, event_type: int, **kwargs: dict[str, Any]):
		pygame.event.post(pygame.event.Event(event_type, kwargs))
