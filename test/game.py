import pygame

import pygbase


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIManager()
		self.button_frame = self.ui.add_frame(pygbase.VerticalScrollingFrame(
			(pygbase.UIValue(0.02, False), pygbase.UIValue(0.02, False)),
			(pygbase.UIValue(0.4, False), pygbase.UIValue(0.96, False)),
			5,
			bg_colour=(50, 50, 50, 100)
		))

		self.button_frame.add_element(pygbase.Button(
			(pygbase.UIValue(0, False), pygbase.UIValue(0, False)),
			(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
			"image",
			"button",
			self.button_frame,
			print, callback_args=("Button Pressed!",),
			text="Click"
		))

		from particle_playground import ParticlePlayground
		self.button_frame.add_element(
			pygbase.Button(
				(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
				"image",
				"button",
				self.button_frame,
				self.set_next_state_type,
				callback_args=(ParticlePlayground, ()),
				text="Particle"
			),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		self.button_frame.add_element(
			pygbase.TextSelectionMenu(
				(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(1, False), pygbase.UIValue(0.1, False)),
				"image",
				["1", "2", "3", "4", "5", "6", "7", "8", "9"],
				self.button_frame
			),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		self.button_frame.add_element(
			pygbase.TextSelectionMenu(
				(pygbase.UIValue(0.1, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(0.8, False), pygbase.UIValue(0.1, False)),
				"image",
				["1", "2", "3", "4", "5", "6", "7", "8", "9"],
				self.button_frame
			),
			align_with_previous=(False, False),
			add_on_to_previous=(False, True)
		)

		self.ui.add_element(
			pygbase.TextElement((pygbase.UIValue(0.5, False), pygbase.UIValue(0.1, False)), "arial", pygbase.UIValue(0.1, False), "white", "Test", self.ui.base_container)
		)

		self.left_image: pygbase.Image = pygbase.ResourceManager.get_resource("image", "left")

	def update(self, delta: float):
		self.ui.update(delta)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((20, 20, 20))

		self.ui.draw(screen)

		self.left_image.draw(screen, (400, 400), 20, (False, False))
		self.left_image.draw(screen, (400, 500), 20, (True, False))
		self.left_image.draw(screen, (400, 600), 20, (False, True))
		self.left_image.draw(screen, (400, 700), 20, (True, True))
