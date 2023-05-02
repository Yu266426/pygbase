import pygame

import pygbase


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIManager()
		self.button_frame = self.ui.add_frame(pygbase.Frame((0.02, 0.02), (0.4, 0.96), bg_colour=(50, 50, 50, 100)))

		self.button_frame.add_element(pygbase.Button((0, 0), (1, 0), pygbase.Common.get_resource_type("image"), "button", print, ("Button Pressed!",), self.button_frame, text="Button"))

		from particle_playground import ParticlePlayground
		self.button_frame.add_element(
			pygbase.Button((0, 0.01), (1, 0), pygbase.Common.get_resource_type("image"), "button", self.set_next_state_type, (ParticlePlayground, ()), self.button_frame, text="Particle"),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		self.button_frame.add_element(
			pygbase.TextSelectionMenu((0, 0.01), (1, 0.1), pygbase.Common.get_resource_type("image"), ["first", "second"], self.button_frame),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		self.ui.add_element(
			pygbase.TextElement((0.5, 0.1), "arial", 0.1, "white", "Test", self.ui.base_container)
		)

	def update(self, delta: float):
		self.ui.update(delta)

		if pygbase.InputManager.keys_down[pygame.K_ESCAPE]:
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((20, 20, 20))

		self.ui.draw(screen)
