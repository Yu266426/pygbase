import gc
import logging

import pygame

import pygbase


class Menu(pygbase.GameState, name="menu"):
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
				text="Particle Testing"
			),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		from dialogue_testing import DialogueTesting
		self.button_frame.add_element(
			pygbase.Button(
				(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
				"image",
				"button",
				self.button_frame,
				self.set_next_state_type,
				callback_args=(DialogueTesting, ()),
				text="Dialogue"
			),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		self.button_frame.add_element(
			pygbase.TextSelectionMenu(
				(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(1, False), pygbase.UIValue(0.1, False)),
				"image",
				["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "OVER NINE THOUSAND"],
				self.button_frame
			),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		self.text_selection_menu = self.button_frame.add_element(
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

		self.progress_bar = self.button_frame.add_element(
			pygbase.ProgressBar(
				(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
				(pygbase.UIValue(1, False), pygbase.UIValue(0.1, False)),
				int(self.text_selection_menu.current_option) / 9,
				pygbase.UIValue(5),
				"green",
				(0, 0, 0, 100),
				self.button_frame,
			), add_on_to_previous=(False, True)
		)

		text_1 = self.ui.add_element(
			pygbase.TextElement((pygbase.UIValue(0.2, False), pygbase.UIValue(0.1, False)), "arial", pygbase.UIValue(0.1, False), "white", "Test1", self.ui.base_container)
		)

		text_2 = self.ui.add_element(
			pygbase.TextElement((pygbase.UIValue(0), pygbase.UIValue(0.1, False)), "arial", pygbase.UIValue(0.1, False), "white", "Test2", self.ui.base_container),
			align_with_previous=(True, False),
			add_on_to_previous=(False, True)
		)

		print(text_1.pos)
		print(text_2.pos)

		self.left_image: pygbase.Image = pygbase.ResourceManager.get_resource("image", "left")

	def update(self, delta: float):
		self.ui.update(delta)

		self.progress_bar.set_fill_percent(int(self.text_selection_menu.current_option) / 9)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_SPACE):
			self.button_frame.ui_pos = (
				self.button_frame.ui_pos[0].add(pygbase.UIValue(0.05, False), self.ui.base_container.size.x),
				self.button_frame.ui_pos[1]
			)

			self.button_frame.reposition()

			self.text_selection_menu.ui_pos = (
				self.text_selection_menu.ui_pos[0].add(pygbase.UIValue(0.05, False), self.button_frame.size.x),
				self.text_selection_menu.ui_pos[1]
			)

			self.text_selection_menu.reposition()

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, surface: pygame.Surface):
		surface.fill((20, 20, 20))

		self.ui.draw(surface)

		self.left_image.draw(surface, (400, 400), 20, (False, False))
		self.left_image.draw(surface, (400, 500), 20, (True, False))
		self.left_image.draw(surface, (400, 600), 20, (False, True))
		self.left_image.draw(surface, (400, 700), 20, (True, True))
