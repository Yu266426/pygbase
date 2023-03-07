import pygame

from pygbase import GameState, InputManager, EventManager
from pygbase.ui.screen import UIScreen
from pygbase.ui.element import Frame, Button


class Game(GameState):
	def __init__(self):
		super().__init__(1)

		print("Loaded game")

		self.ui = UIScreen()
		self.button_frame = self.ui.add_frame(Frame((20, 20), (400, 760), bg_colour=(50, 50, 50, 100)))
		self.button_frame.add_element(Button((0, 0), 1, "button", self.button_pressed, text="Test", size=(400, None)))

	def button_pressed(self):
		print("Button Pressed!")

	def update(self, delta: float):
		self.ui.update(delta)

		if InputManager.keys_down[pygame.K_ESCAPE]:
			EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((20, 20, 20))

		self.ui.draw(screen)
