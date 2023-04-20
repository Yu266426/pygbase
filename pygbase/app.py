from typing import Type, Union, Optional

import pygame

from .common import Common
from .events import EventManager
from .game_state import GameState
from .inputs import InputManager
from .loader import Loading


class App:
	def __init__(self, after_load_state: Type[GameState], title: Optional[str] = None, flags=pygame.SCALED, vsync=True):
		self.is_running: bool = True

		self.window: pygame.Surface = pygame.display.set_mode((Common.get_value("screen_width"), Common.get_value("screen_height")), flags=flags, vsync=vsync)
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.title = title
		if self.title is not None:
			pygame.display.set_caption(self.title)

		self.game_state: Union[Loading, GameState] = Loading(after_load_state)

		EventManager.add_handler("all", pygame.QUIT, self.quit_handler)

	def quit_handler(self, event: pygame.event.Event):
		self.is_running = False

	def handle_events(self):
		InputManager.reset()
		EventManager.handle_events(self.game_state.id)

	def update(self):
		delta = min(self.clock.tick() / 1000, 0.12)

		if self.title is None:
			pygame.display.set_caption(f"fps: {round(self.clock.get_fps())}, delta: {delta}")

		self.game_state.update(delta)

	def draw(self):
		self.game_state.draw(self.window)

		pygame.display.flip()

	def switch_state(self):
		self.game_state = self.game_state.get_next_state()

	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.draw()
			self.switch_state()
