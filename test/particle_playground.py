import pygame

import pygbase

from game import Game


class ParticlePlayground(pygbase.GameState, name="particles"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIScreen()
		self.button_frame = self.ui.add_frame(pygbase.Frame((20, 20), (100, 50), bg_colour=(50, 50, 50, 100)))
		self.button_frame.add_element(
			pygbase.Button(
				(0, 0), pygbase.Common.get_resource_type("image"), "button",
				self.set_next_state_type, (Game, ()),
				size=(100, 50),
				text="Back"
			)
		)

	def update(self, delta: float):
		self.ui.update(delta)

	def draw(self, screen: pygame.Surface):
		screen.fill((20, 20, 20))
		self.ui.draw(screen)
