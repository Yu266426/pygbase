import logging
from typing import Optional, Union, Callable

import pygame

from .. import Common
from ..graphics.image import Image
from ..inputs import InputManager
from ..resources import ResourceManager
from ..ui.text import Text


class UIElement:
	def __init__(self, percent_pos: tuple[float, float], percent_size: tuple[float, float]):
		# Validate ranges
		if not (0 <= percent_pos[0] <= 1):
			logging.error(f"Percent pos x: {percent_pos[0]} is not in range")
			raise ValueError(f"Percent pos x: {percent_pos[0]} is not in range")
		if not (0 <= percent_pos[1] <= 1):
			logging.error(f"Percent pos y: {percent_pos[1]} is not in range")
			raise ValueError(f"Percent pos y: {percent_pos[1]} is not in range")

		if not (0 <= percent_size[0] <= 1):
			logging.error(f"Percent size width: {percent_pos[0]} is not in range")
			raise ValueError(f"Percent size width: {percent_pos[0]} is not in range")
		if not (0 <= percent_size[1] <= 1):
			logging.error(f"Percent size height: {percent_pos[1]} is not in range")
			raise ValueError(f"Percent size height: {percent_pos[1]} is not in range")

		# Percent size of container
		self.percent_pos: tuple[float, float] = percent_pos
		self.percent_size: tuple[float, float] = percent_size

		# Defaults size to screen, but is later changed if added to a frame
		self.pos: pygame.Vector2 = pygame.Vector2(
			Common.get_value("screen_width") * self.percent_pos[0],
			Common.get_value("screen_height") * self.percent_pos[1]
		)
		self.size: pygame.Vector2 = pygame.Vector2(
			Common.get_value("screen_width") * self.percent_size[0],
			Common.get_value("screen_height") * self.percent_size[1]
		)

		self.rect = pygame.Rect(self.pos, self.size)

	def added_to_frame(self, frame: "Frame"):
		self.pos.update(
			frame.size.x * self.percent_pos[0],
			frame.size.y * self.percent_pos[1]
		)

		self.size.update(
			frame.size.x * self.percent_size[0],
			frame.size.y * self.percent_size[1]
		)

		self.rect.topleft = self.pos + frame.pos
		self.rect.size = self.size

	def update(self, delta: float):
		pass

	def draw(self, screen: pygame.Surface):
		pass


class Frame(UIElement):
	def __init__(self, percent_pos: tuple[float, float], percent_size: tuple[float, float], bg_colour=None):
		super().__init__(percent_pos, percent_size)

		self.active = True

		self.bg = None
		if bg_colour is not None:
			self.bg = pygame.Surface(self.size, flags=pygame.SRCALPHA)
			self.bg.fill(bg_colour)

		self.elements: list[UIElement] = []

	def added_to_frame(self, frame: "Frame"):
		super().added_to_frame(frame)

		for f_element in self.elements:
			f_element.rect.x += frame.rect.x
			f_element.rect.y += frame.rect.y

	def add_element(self, element: UIElement, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> "Frame":
		# Align
		if align_with_previous[0]:
			element.percent_pos = self.elements[-1].percent_pos[0], element.percent_pos[1]

		if align_with_previous[1]:
			element.percent_pos = element.percent_pos[0], self.elements[-1].percent_pos[1]

		# Add on
		if add_on_to_previous[0]:
			element.percent_pos = self.elements[-1].percent_pos[0] + self.elements[-1].percent_size[0] + element.percent_pos[0], element.percent_pos[1]

		if add_on_to_previous[1]:
			element.percent_pos = element.percent_pos[0], self.elements[-1].percent_pos[1] + self.elements[-1].percent_size[1] + element.percent_pos[1]

		element.added_to_frame(self)

		out_of_bounds = False

		# If element does not go out of frame, add it to the frame
		if 0 <= element.pos[0] and element.pos[0] + element.size[0] <= self.size[0]:
			if 0 <= element.pos[1] and element.pos[1] + element.size[1] <= self.size[1]:
				self.elements.append(element)
			else:
				out_of_bounds = True
		else:
			out_of_bounds = True

		if out_of_bounds:
			logging.warning(f"Element <{type(element).__name__}>(size: {element.size}, pos: {element.pos}) is not contained within frame (size: {self.size})")

		return self

	def update(self, delta: float):
		if self.active:
			for element in self.elements:
				element.update(delta)

	def draw(self, screen: pygame.Surface):
		if self.active:
			if self.bg is not None:
				screen.blit(self.bg, self.rect)

			for element in self.elements:
				element.draw(screen)


class ImageElement(UIElement):
	def __init__(self, percent_pos: tuple[float, float], percent_size: tuple[float, float], resource_type: int, resource_name: str, alignment: str = "l"):
		super().__init__(percent_pos, percent_size)

		self.image: Image = ResourceManager.get_resource(resource_type, resource_name)
		self.alignment = alignment

	def added_to_frame(self, frame: "Frame"):
		image_size = self.image.get_image().get_size()

		if self.percent_size[0] != 0 and self.percent_size[1] != 0:
			self.image: Image = self.image.scale((frame.size.x * self.percent_size[0], frame.size.y * self.percent_size[1]))
		elif self.percent_size[0] != 0:
			new_width = frame.size[0] * self.percent_size[0]

			self.image: Image = self.image.scale((new_width, new_width * image_size[1] / image_size[0]))
		elif self.percent_size[1] != 0:
			new_height = frame.size[1] * self.percent_size[1]

			self.image: Image = self.image.scale((new_height * image_size[0] / image_size[1], new_height))

		self.percent_size = (
			self.image.get_image().get_width() / frame.size[0],
			self.image.get_image().get_height() / frame.size[1]
		)

		if self.alignment == "l":
			# Position unchanged
			pass
		elif self.alignment == "r":
			self.percent_pos = (
				self.percent_pos[0] - self.percent_size[0],
				self.percent_pos[1]
			)
		elif self.alignment == "c":
			self.percent_pos = (
				self.percent_pos[0] - self.percent_size[0] / 2,
				self.percent_pos[1]
			)
		else:
			raise ValueError(f"center: `{self.alignment}` on {self.__class__.__name__} is not valid")

		super().added_to_frame(frame)

	def draw(self, screen: pygame.Surface):
		self.image.draw(screen, self.rect)


class Button(UIElement):
	def __init__(
			self,
			percent_pos: tuple[float, float],
			percent_size: tuple[float, float],
			resource_type: int,
			resource_name: str,
			callback: Callable[..., None],
			callback_args: tuple,
			text: str = "",
			text_colour="white",
			font: str = "arial",
			alignment: str = "l"
	):
		super().__init__(percent_pos, percent_size)

		self.image: Image = ResourceManager.get_resource(resource_type, resource_name)

		self.alignment = alignment

		self.callback = callback
		self.callback_args = callback_args

		self.mouse_on = False

		self.highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.highlight.fill((255, 255, 255, 40))

		self.text: Union[Text, str] = text
		self.text_colour = text_colour
		self.font = font

	def added_to_frame(self, frame: "Frame"):
		image_size = self.image.get_image().get_size()

		if self.percent_size[0] != 0 and self.percent_size[1] != 0:
			self.image: Image = self.image.scale((frame.size.x * self.percent_size[0], frame.size.y * self.percent_size[1]))
		elif self.percent_size[0] != 0:
			new_width = frame.size[0] * self.percent_size[0]

			self.image: Image = self.image.scale((new_width, new_width * image_size[1] / image_size[0]))
		elif self.percent_size[1] != 0:
			new_height = frame.size[1] * self.percent_size[1]

			self.image: Image = self.image.scale((new_height * image_size[0] / image_size[1], new_height))

		self.percent_size = (
			self.image.get_image().get_width() / frame.size[0],
			self.image.get_image().get_height() / frame.size[1]
		)

		self.highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.highlight.fill((255, 255, 255, 40))

		if self.alignment == "l":
			# Position unchanged
			pass
		elif self.alignment == "r":
			self.percent_pos = (
				self.percent_pos[0] - self.percent_size[0],
				self.percent_pos[1]
			)
		elif self.alignment == "c":
			self.percent_pos = (
				self.percent_pos[0] - self.percent_size[0] / 2,
				self.percent_pos[1]
			)
		else:
			raise ValueError(f"center: `{self.alignment}` on {self.__class__.__name__} is not valid")

		super().added_to_frame(frame)

		self.text = Text((self.rect.centerx, self.rect.top + self.rect.height * 0.2), self.font, self.size[1] * 0.7, self.text_colour, self.text, use_sys=True)

	def update(self, delta: float):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.mouse_on = True

			if InputManager.mouse_up[0]:
				if self.callback is not None:
					self.callback(*self.callback_args)
		else:
			self.mouse_on = False

	def draw(self, screen: pygame.Surface):
		self.image.draw(screen, self.rect)
		self.text.draw(screen, "c")

		if self.mouse_on:
			screen.blit(self.highlight, self.rect)


# TODO: Change these to use percentages
class TextElement(UIElement):
	def __init__(self, pos: tuple, font_name: str, height: int | float, colour, text: str, centered=False, use_sys=True):
		super().__init__(pos, (0, height))

		self.text = Text(pos, font_name, height * 1.25, colour, text, use_sys=use_sys)

		self.centered = centered

	def set_text(self, new_text: str):
		self.text.set_text(new_text)

	def draw(self, screen: pygame.Surface):
		render_surface = pygame.Surface(self.text.rendered_text[1].size).convert_alpha()
		render_surface.fill((0, 0, 0, 0))
		self.text.draw(render_surface, pos=(0, 0))
		self.rect.width = render_surface.get_width()

		offset = 0
		if self.centered:
			offset = self.rect.width / 2
		screen.blit(render_surface, (self.rect.x - offset, self.rect.y))


class TextSelectionMenu(Frame):
	def __init__(self, pos: tuple, size: tuple, image_resource_type: int, options: list):
		super().__init__(pos, size, bg_colour=(0, 0, 0, 150))

		self.options = options

		self.index: int = 0
		self.current_option = self.options[self.index]

		self.add_element(Button((0, 0), image_resource_type, "left", self.change_option, (-1,), size=(None, self.rect.height)))
		self.add_element(Button((self.rect.width, 0), image_resource_type, "right", self.change_option, (1,), size=(None, self.rect.height), alignment="r"))

		self.text = TextElement((self.rect.width / 2, self.rect.height * 0.3 / 2), "arial", self.rect.height * 0.7, (255, 255, 255), self.current_option, centered=True)
		self.add_element(self.text)

	def change_option(self, direction):
		self.index += direction

		if self.index < 0:
			self.index = len(self.options) - 1
		elif len(self.options) <= self.index:
			self.index = 0

		self.current_option = self.options[self.index]

		self.text.set_text(self.current_option)
