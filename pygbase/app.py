import gc
import logging
from typing import Type, Union, Callable

import pygame

from .common import Common
from .debug import Debug
from .events import Events
from .game_state import GameState
from .inputs import Inputs
from .loader import Loading


class App:
	def __init__(
			self,
			after_load_state: Type[GameState],
			title: str = "Pygbase Window",
			flags=0,
			vsync=True,
			fixed_time_fps: int = 60,
			run_on_load_complete: tuple[Callable, ...] = ()
	):
		self.is_running: bool = True

		self.title = title

		# TODO: add flag handling and vsync
		# ^ This is dependent partly on pygame though :/
		self.window = pygame.Window(title, Common.get_value("screen_size"))
		self.screen: pygame.Surface = self.window.get_surface()
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.game_state: Union[Loading, GameState] = Loading(after_load_state, run_on_load_complete)

		self.fixed_time_rate = 1 / fixed_time_fps

		Events.add_handler("all", pygame.QUIT, self.quit_handler)

	def quit_handler(self, event: pygame.event.Event):
		self.is_running = False

	def handle_events(self):
		Inputs.reset()
		Events.handle_events(self.game_state.id)

	def update(self, delta):
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
			Debug.clear()

			# Update
			self.update(delta)
			while update_timer >= self.fixed_time_rate:
				self.fixed_update()
				update_timer -= self.fixed_time_rate

			# Drawing
			Debug.update_timing_text(delta, round(self.clock.get_fps()))

			self.draw()
			Debug.draw(self.screen)
			self.window.flip()

			# State check
			self.switch_state()
