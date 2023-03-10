from typing import Type, Union

import pygame.display

from .common import Common
from .events import EventManager
from .game_state import GameState
from .inputs import InputManager
from .loader import Loading


class App:
	def __init__(self, after_load_state: Type[GameState], flags=pygame.SCALED, vsync=True):
		self.is_running: bool = True

		self.window: pygame.Surface = pygame.display.set_mode((Common.get_value("screen_width"), Common.get_value("screen_height")), flags=flags, vsync=vsync)
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.game_state: Union[Loading, GameState] = Loading(after_load_state)

		EventManager.add_handler(0, pygame.QUIT, self.quit_handler)

	def quit_handler(self, event: pygame.event.Event):
		self.is_running = False

	def handle_events(self):
		InputManager.reset()
		EventManager.handle_events(self.game_state.id)

	def update(self):
		self.clock.tick()
		pygame.display.set_caption(f"{round(self.clock.get_fps())}")

		self.game_state.update(self.clock.get_time() / 1000)

	def draw(self):
		self.game_state.draw(self.window)

		pygame.display.flip()

	def switch_state(self):
		self.game_state = self.game_state.next_state()

	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.draw()
			self.switch_state()
