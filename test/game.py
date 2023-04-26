import pygame

import pygbase


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIScreen()
		self.button_frame = self.ui.add_frame(pygbase.Frame((20, 20), (400, 760), bg_colour=(50, 50, 50, 100)))
		self.button_frame.add_element(pygbase.Button((0, 0), 1, "button", self.button_pressed, (), text="Test", size=(400, None)))
		from particle_playground import ParticlePlayground
		self.button_frame.add_element(
			pygbase.Button((0, 20), pygbase.Common.get_resource_type("image"), "button", self.set_next_state_type, (ParticlePlayground, ()), text="Particle", size=(400, None)),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

	def button_pressed(self):
		print("Button Pressed!")

	def update(self, delta: float):
		self.ui.update(delta)

		if pygbase.InputManager.keys_down[pygame.K_ESCAPE]:
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((20, 20, 20))

		self.ui.draw(screen)
