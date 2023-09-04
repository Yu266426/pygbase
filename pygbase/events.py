from typing import Callable, Any

import pygame

from .common import Common


class EventManager:
	_handlers: dict[int, dict[int, list[Callable[[pygame.event.Event], None]]]] = {}
	_custom_events: dict[str, int] = {}

	@classmethod
	def init(cls):
		cls._handlers[Common.get_game_state_id("all")] = {}

	@classmethod
	def create_custom_event(cls, name: str):
		if name not in cls._custom_events:
			cls._custom_events[name] = pygame.event.custom_type()
		else:
			raise ValueError(f"Event `{name}` already exists")

	@classmethod
	def add_handler(cls, state_name: str, event: int | str, handler: Callable[[pygame.event.Event], None]):
		game_state_id = Common.get_game_state_id(state_name)

		if game_state_id not in cls._handlers:
			cls._handlers[game_state_id] = {}

		if isinstance(event, str):
			event_type = cls._custom_events[event]
		elif isinstance(event, int):
			event_type = event
		else:
			raise TypeError("Event must be of type int or str")

		if event_type not in cls._handlers[game_state_id]:
			cls._handlers[game_state_id][event_type] = []

		cls._handlers[game_state_id][event_type].append(handler)

	@classmethod
	def handle_events(cls, current_game_state: int):
		"""
		Used by the app
		"""

		for event in pygame.event.get():
			if current_game_state in cls._handlers:
				if event.type in cls._handlers[current_game_state]:
					for handler in cls._handlers[current_game_state][event.type]:
						handler(event)

			if event.type in cls._handlers[0]:
				for handler in cls._handlers[0][event.type]:
					handler(event)

	# TODO: Determine if this is needed
	@classmethod
	def run_handlers(cls, state_name: str, event_type: int, **kwargs):
		game_state_id = Common.get_game_state_id(state_name)

		for handler in cls._handlers[game_state_id][event_type]:
			handler(pygame.event.Event(event_type, kwargs))

	@classmethod
	def post_event(cls, event: int | str, **kwargs: dict[str, Any]):
		if isinstance(event, int):
			pygame.event.post(pygame.event.Event(event, kwargs))
		elif isinstance(event, str):
			if event in cls._custom_events:
				pygame.event.post(pygame.event.Event(cls._custom_events[event], kwargs))
			else:
				raise ValueError(f"Event `{event}` does not exist")
		else:
			raise TypeError("Event must be of type int or str")
