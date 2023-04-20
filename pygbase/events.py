from typing import Callable, Any

import pygame

from .common import Common


class EventManager:
	handlers: dict[int, dict[int, list[Callable[[pygame.event.Event], None]]]] = {}

	@classmethod
	def init(cls):
		cls.handlers[Common.get_game_state_id("all")] = {}

	@classmethod
	def add_handler(cls, state_name: str, event_type: int, handler: Callable[[pygame.event.Event], None]):
		game_state_id = Common.get_game_state_id(state_name)

		if game_state_id not in cls.handlers:
			cls.handlers[game_state_id] = {}

		if event_type not in cls.handlers[game_state_id]:
			cls.handlers[game_state_id][event_type] = []

		cls.handlers[game_state_id][event_type].append(handler)

	@classmethod
	def handle_events(cls, current_game_state: int):
		for event in pygame.event.get():
			if current_game_state in cls.handlers:
				if event.type in cls.handlers[current_game_state]:
					for handler in cls.handlers[current_game_state][event.type]:
						handler(event)

			if event.type in cls.handlers[0]:
				for handler in cls.handlers[0][event.type]:
					handler(event)

	# TODO: Determine if this is needed
	@classmethod
	def run_handlers(cls, state_name: str, event_type: int, **kwargs):
		game_state_id = Common.get_game_state_id(state_name)

		for handler in cls.handlers[game_state_id][event_type]:
			handler(pygame.event.Event(event_type, kwargs))

	@classmethod
	def post_event(cls, event_type: int, **kwargs: dict[str, Any]):
		pygame.event.post(pygame.event.Event(event_type, kwargs))
