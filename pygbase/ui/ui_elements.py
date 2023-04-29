import logging
from typing import Optional, Union, Callable

import pygame

from ..graphics.image import Image
from ..inputs import InputManager
from ..resources import ResourceManager
from ..ui.text import Text


class UIElement:
	def __init__(self, pos: tuple, size: tuple):
		self.pos = pos
		self.size = size

		self.rect = pygame.Rect(pos, size) if pos[1] is not None else None

	def added_to_frame(self, frame: "Frame"):
		# Offset the rect to frame space
		self.rect.x += frame.rect.x
		self.rect.y += frame.rect.y

	def update(self, delta: float):
		pass

	def draw(self, screen: pygame.Surface):
		pass


class Frame(UIElement):
	def __init__(self, pos: tuple, size: tuple, bg_colour=None):
		super().__init__(pos, size)

		self.active = True

		self.bg = None
		if bg_colour is not None:
			self.bg = pygame.Surface(self.size).convert_alpha()
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
			element.pos = self.elements[-1].pos[0], element.pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		if align_with_previous[1]:
			element.pos = element.pos[0], self.elements[-1].pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		# Add on
		if add_on_to_previous[0]:
			element.pos = self.elements[-1].pos[0] + self.elements[-1].size[0] + element.pos[0], element.pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		if add_on_to_previous[1]:
			element.pos = element.pos[0], self.elements[-1].pos[1] + self.elements[-1].size[1] + element.pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		out_of_bounds = False

		# If element does not go out of frame, add it to the frame
		if 0 <= element.pos[0] and element.pos[0] + element.size[0] <= self.size[0]:
			if 0 <= element.pos[1] and element.pos[1] + element.size[1] <= self.size[1]:
				element.added_to_frame(self)

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
	def __init__(self, pos: tuple, resource_type: int, resource_name: str, size: Optional[tuple] = None, alignment: str = "l"):
		self.image: Image = ResourceManager.get_resource(resource_type, resource_name)

		if size is not None:
			self.image.scale(size)

		if alignment == "l":
			super().__init__(pos, self.image.get_image().get_size())
		elif alignment == "r":
			super().__init__((pos[0] - self.image.get_image().get_width(), pos[1]), self.image.get_image().get_size())
		elif alignment == "c":
			super().__init__((pos[0] - self.image.get_image().get_width() / 2, pos[1]), self.image.get_image().get_size())
		else:
			raise ValueError(f"center: `{alignment}` on {self.__class__.__name__} is not valid")

	def draw(self, screen: pygame.Surface):
		self.image.draw(screen, self.rect)


class Button(UIElement):
	def __init__(
			self,
			pos: tuple,
			resource_type: int,
			resource_name: str,
			callback: Callable[..., None],
			callback_args: tuple,
			size: Optional[tuple] = None,
			text: str = "",
			text_colour="white",
			font: str = "arial",
			alignment: str = "l"
	):
		self.image: Image = ResourceManager.get_resource(resource_type, resource_name)

		if size is not None:
			if size[0] is None:
				self.image = self.image.scale((self.image.get_image().get_width() * size[1] / self.image.get_image().get_height(), size[1]))
			elif size[1] is None:
				self.image = self.image.scale((size[0], self.image.get_image().get_height() * size[0] / self.image.get_image().get_width()))
			else:
				self.image = self.image.scale(size)

		if alignment == "l":
			super().__init__(pos, self.image.get_image().get_size())
		elif alignment == "r":
			super().__init__((pos[0] - self.image.get_image().get_width(), pos[1]), self.image.get_image().get_size())
		elif alignment == "c":
			super().__init__((pos[0] - self.image.get_image().get_width() / 2, pos[1]), self.image.get_image().get_size())
		else:
			raise ValueError(f"center: `{alignment}` on {self.__class__.__name__} is not valid")

		self.callback = callback
		self.callback_args = callback_args

		self.mouse_on = False
		self.highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.highlight.fill((255, 255, 255, 40))

		self.text: Union[Text, str] = text
		self.text_colour = text_colour
		self.font = font

	def added_to_frame(self, frame: "Frame"):
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
