import gc
import logging
from typing import Type, Union, Optional, Callable

import pygame

from .debug import DebugDisplay
from .common import Common
from .events import EventManager
from .game_state import GameState
from .inputs import InputManager
from .loader import Loading


class App:
	def __init__(
			self,
			after_load_state: Type[GameState],
			title: Optional[str] = None,
			flags=0,
			vsync=True,
			fixed_time_fps: int = 60,
			run_on_load_complete: tuple[Callable, ...] = ()
	):
		self.is_running: bool = True

		self.screen: pygame.Surface = pygame.display.set_mode((Common.get_value("screen_width"), Common.get_value("screen_height")), flags=flags, vsync=vsync)
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.title = title
		if self.title is not None:
			pygame.display.set_caption(self.title)

		self.game_state: Union[Loading, GameState] = Loading(after_load_state, run_on_load_complete)

		self.fixed_time_rate = 1 / fixed_time_fps

		EventManager.add_handler("all", pygame.QUIT, self.quit_handler)

	def quit_handler(self, event: pygame.event.Event):
		self.is_running = False

	def handle_events(self):
		InputManager.reset()
		EventManager.handle_events(self.game_state.id)

	def update(self, delta):
		if self.title is None:
			pygame.display.set_caption(f"fps: {round(self.clock.get_fps())}, delta: {delta}")

		self.game_state.update(delta)

	def fixed_update(self):
		self.game_state.fixed_update(self.fixed_time_rate)

	def draw(self):
		self.game_state.draw(self.screen)

	def switch_state(self):
		next_state = self.game_state.get_next_state()
		if self.game_state is not next_state:
			self.game_state.exit()

			self.game_state = self.game_state.get_next_state()
			self.game_state.enter()

			logging.debug("Switching states, running garbage collector...")
			gc.collect()

	def run(self):
		self.is_running = True

		update_timer = 0.0

		while self.is_running:
			# Timing
			delta = min(self.clock.tick() / 1000, 0.12)
			update_timer += delta

			# Events
			self.handle_events()

			# Debug
			DebugDisplay.clear()

			# Update
			self.update(delta)
			while update_timer >= self.fixed_time_rate:
				self.fixed_update()
				update_timer -= self.fixed_time_rate

			# Drawing
			self.draw()
			DebugDisplay.draw(self.screen)
			pygame.display.flip()

			# State check
			self.switch_state()
