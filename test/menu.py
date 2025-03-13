import pygame

import pygbase
from pygbase.ui import *


class Menu(pygbase.GameState, name="menu"):
	def __init__(self):
		super().__init__()

		from particle_playground import ParticlePlayground
		from dialogue_testing import DialogueTesting
		from tweens import Tweens
		with Frame(size=(Grow(), Grow()), padding=Padding.all(10)) as ui:
			with Frame(size=(250, Grow()), layout=Layout.TOP_TO_BOTTOM, padding=Padding.all(5), gap=10, bg_color=(50, 50, 50, 100)) as button_frame:
				with Button(print, callback_args=("Button Pressed!",), size=(Grow(), Fit())):
					with Image("image/button", size=(Grow(), Fit()), x_align=XAlign.CENTER, y_align=YAlign.CENTER):
						Text("Click", 30, "white")

				with Button(self.set_next_state_type, callback_args=(ParticlePlayground, ()), size=(Grow(), Fit())):
					with Image("image/button", size=(Grow(), Fit()), x_align=XAlign.CENTER, y_align=YAlign.CENTER):
						Text("Particles", 30, "white")

				with Button(self.set_next_state_type, callback_args=(DialogueTesting, ()), size=(Grow(), Fit())):
					with Image("image/button", size=(Grow(), Fit()), x_align=XAlign.CENTER, y_align=YAlign.CENTER):
						Text("Dialogue", 30, "white")

				with Button(self.set_next_state_type, callback_args=(Tweens, ()), size=(Grow(), Fit())):
					with Image("image/button", size=(Grow(), Fit()), x_align=XAlign.CENTER, y_align=YAlign.CENTER):
						Text("Tweens", 30, "white")

		self.ui = ui
		self.button_frame = button_frame

		# self.button_frame.add_element(
		# 	pygbase.TextSelectionMenu(
		# 		(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
		# 		(pygbase.UIValue(1, False), pygbase.UIValue(0.1, False)),
		# 		"image",
		# 		["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "OVER NINE THOUSAND"],
		# 		self.button_frame
		# 	),
		# 	align_with_previous=(True, False),
		# 	add_on_to_previous=(False, True)
		# )
		#
		# self.text_selection_menu = self.button_frame.add_element(
		# 	pygbase.TextSelectionMenu(
		# 		(pygbase.UIValue(0.1, False), pygbase.UIValue(0.01, False)),
		# 		(pygbase.UIValue(0.8, False), pygbase.UIValue(0.1, False)),
		# 		"image",
		# 		["1", "2", "3", "4", "5", "6", "7", "8", "9"],
		# 		self.button_frame
		# 	),
		# 	align_with_previous=(False, False),
		# 	add_on_to_previous=(False, True)
		# )
		#
		# self.progress_bar = self.button_frame.add_element(
		# 	pygbase.ProgressBar(
		# 		(pygbase.UIValue(0, False), pygbase.UIValue(0.01, False)),
		# 		(pygbase.UIValue(1, False), pygbase.UIValue(0.1, False)),
		# 		int(self.text_selection_menu.current_option) / 9,
		# 		pygbase.UIValue(5),
		# 		"green",
		# 		(0, 0, 0, 100),
		# 		self.button_frame,
		# 	), add_on_to_previous=(False, True)
		# )
		#
		# text_1 = self.ui.add_element(
		# 	pygbase.TextElement((pygbase.UIValue(0.7, False), pygbase.UIValue(0.1, False)), "arial", pygbase.UIValue(0.1, False), "white", "Test1", self.ui.base_container)
		# )
		#
		# text_2 = self.ui.add_element(
		# 	pygbase.TextElement((pygbase.UIValue(0), pygbase.UIValue(20)), "arial", pygbase.UIValue(0.1, False), "white", "Test2", self.ui.base_container, alignment=pygbase.UIAlignment.TOP_RIGHT),
		# 	align_with_previous=(True, False),
		# 	add_on_to_previous=(False, True)
		# )

		# print(text_1.pos)
		# print(text_2.pos)

		self.left_image: pygbase.Image = pygbase.Resources.get_resource("image", "left")

	def update(self, delta: float):
		self.ui.update(delta)

		# self.progress_bar.set_fill_percent(int(self.text_selection_menu.current_option) / 9)
		#
		# if pygbase.Input.key_just_pressed(pygame.K_SPACE):
		# 	self.button_frame.ui_pos = (
		# 		self.button_frame.ui_pos[0].add(pygbase.UIValue(0.05, False), self.ui.base_container.size.x),
		# 		self.button_frame.ui_pos[1]
		# 	)
		#
		# 	self.button_frame.reposition()
		#
		# 	self.text_selection_menu.ui_pos = (
		# 		self.text_selection_menu.ui_pos[0].add(pygbase.UIValue(0.05, False), self.button_frame.size.x),
		# 		self.text_selection_menu.ui_pos[1]
		# 	)
		#
		# 	self.text_selection_menu.reposition()

		if pygbase.Input.key_just_pressed(pygame.K_ESCAPE):
			pygbase.Events.post_event(pygame.QUIT)

	def draw(self, surface: pygame.Surface):
		surface.fill((20, 20, 20))

		self.ui.draw(surface)
		# sys.exit()

		self.left_image.draw(surface, (400, 400), 20, flip=(False, False))
		self.left_image.draw(surface, (400, 500), 20, flip=(True, False))
		self.left_image.draw(surface, (400, 600), 20, flip=(False, True))
		self.left_image.draw(surface, (400, 700), 20, flip=(True, True))
