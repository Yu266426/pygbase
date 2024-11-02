from typing import Callable

import pygame

from .common import Common


class Events:
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
	def _convert_to_event_type(cls, event: int | str) -> int:
		if isinstance(event, str):
			return cls._custom_events[event]
		elif isinstance(event, int):
			return event
		else:
			raise TypeError("Event must be of type int or str")

	@classmethod
	def add_handler(cls, state_name: str, event: int | str, handler: Callable[[pygame.event.Event], None]):
		game_state_id = Common.get_game_state_id(state_name)

		if game_state_id not in cls._handlers:
			cls._handlers[game_state_id] = {}

		event_type = cls._convert_to_event_type(event)

		if event_type not in cls._handlers[game_state_id]:
			cls._handlers[game_state_id][event_type] = []

		cls._handlers[game_state_id][event_type].append(handler)

	@classmethod
	def remove_handler(cls, handler: Callable[[pygame.event.Event], None], state_name: str | None = None, event: int | str | None = None):
		if state_name is not None:
			game_state_id = Common.get_game_state_id(state_name)

			if event is not None:
				cls._handlers[game_state_id][cls._convert_to_event_type(event)].remove(handler)
			else:
				for _event_type, handlers in cls._handlers[game_state_id].items():
					if handler in handlers:
						handlers.remove(handler)
		else:
			for _game_state_id, events in cls._handlers.items():
				for _event_type, handlers in events.items():
					if handler in handlers:
						handlers.remove(handler)

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
	def post_event(cls, event: int | str, **kwargs):
		if isinstance(event, int):
			pygame.event.post(pygame.event.Event(event, kwargs))
		elif isinstance(event, str):
			if event in cls._custom_events:
				pygame.event.post(pygame.event.Event(cls._custom_events[event], kwargs))
			else:
				raise ValueError(f"Event `{event}` does not exist")
		else:
			raise TypeError("Event must be of type int or str")
