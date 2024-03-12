import logging
from typing import Optional, Callable

import pygame

from .text import Text
from .ui_element import UIElement, UIElementType
from .values import UIActionTriggers, UIValue, UIAlignment
from ..graphics.image import Image
from ..inputs import InputManager
from ..resources import ResourceManager


class Frame(UIElement):
	def __init__(self, pos: tuple[UIValue, UIValue], size: tuple[UIValue, UIValue], container: Optional["Frame"] = None, bg_colour=None):
		super().__init__(pos, size, container)

		self.active: bool = True

		self.surface = pygame.Surface(self._size, flags=pygame.SRCALPHA)

		self.bg_colour = bg_colour
		self.bg: Optional[pygame.Surface] = None

		if self.bg_colour is not None:
			self.bg = pygame.Surface(self._size, flags=pygame.SRCALPHA)
			self.bg.fill(self.bg_colour)

		self.elements: list[UIElementType] = []

	def reposition(self):
		super().reposition()

		for element in self.elements:
			element.reposition()

	def add_element(self, element: UIElementType, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> UIElementType:
		if len(self.elements) > 0:
			prev_element = self.elements[-1]
			# Align
			if align_with_previous[0]:
				element.ui_pos = prev_element.ui_pos[0], element.ui_pos[1]

			if align_with_previous[1]:
				element.ui_pos = element.ui_pos[0], prev_element.ui_pos[1]

			# Add on
			if add_on_to_previous[0]:
				element.ui_pos = (
					prev_element.ui_pos[0].add(prev_element.ui_size[0], prev_element.container_size[0]).add(element.ui_pos[0], prev_element.container_size[0]),
					element.ui_pos[1]
				)

			if add_on_to_previous[1]:
				element.ui_pos = (
					element.ui_pos[0],
					prev_element.ui_pos[1].add(prev_element.ui_size[1], prev_element.container_size[1]).add(element.ui_pos[1], prev_element.container_size[1])
				)

		element.reposition()

		# If element does not go out of frame, add it to the frame
		if not (0 <= element._pos[0] and element._pos[0] + element.size[0] <= self._size[0]):
			logging.warning(f"Element <{type(element).__name__}>(size: {element.size}, pos: {element._pos}) is not contained within frame (size: {self._size})")

		if not (0 <= element._pos[1] and element._pos[1] + element.size[1] <= self._size[1]):
			logging.warning(f"Element <{type(element).__name__}>(size: {element.size}, pos: {element._pos}) is not contained within frame (size: {self._size})")

		self.elements.append(element)

		# return self
		return element

	def remove_element(self, element: UIElementType):
		self.elements.remove(element)

	def clear(self):
		self.elements.clear()

	def update(self, delta: float):
		super().update(delta)

		if self.active:
			for element in self.elements:
				element.update(delta)

	def draw(self, surface: pygame.Surface):
		if self.active:
			self.surface.fill((0, 0, 0, 0))

			if self.bg is not None:
				self.surface.blit(self.bg, (0, 0))

			for element in self.elements:
				element.draw(self.surface)

			surface.blit(self.surface, self.pos)


class VerticalScrollingFrame(Frame):
	def __init__(self, pos: tuple[UIValue, UIValue], size: tuple[UIValue, UIValue], scroll_speed, container: Optional["Frame"] = None, bg_colour=None):
		super().__init__(pos, size, container=container, bg_colour=bg_colour)

		self.scroll_speed = scroll_speed

		self.scroll_offset = 0

		self.top_element: Optional[UIElement] = None
		self.bottom_element: Optional[UIElement] = None

		self.add_action(UIActionTriggers.ON_SCROLL_Y, self.on_scroll)

	def add_element(self, element: UIElementType, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> UIElementType:
		super().add_element(element, align_with_previous, add_on_to_previous)

		if self.top_element is None:
			self.top_element = element
			self.bottom_element = element
		else:
			if element.pos.y < self.top_element.pos.y:
				self.top_element = element
			if element.pos.y > self.bottom_element.pos.y:
				self.bottom_element = element

		return element

	def on_scroll(self):
		if self.top_element is not None and self.bottom_element is not None:
			scroll = InputManager.get_scroll_y()

			for element in self.elements:
				element.ui_pos = element.ui_pos[0], UIValue(element.ui_pos[1].get_pixels(self.rect.height) + scroll * self.scroll_speed)
				element.reposition()

			if self.top_element.pos.y > 0:
				offset = self.top_element.pos.y

				for element in self.elements:
					element.ui_pos = element.ui_pos[0], UIValue(element.ui_pos[1].get_pixels(self.rect.height) - offset)
					element.reposition()

			if self.bottom_element.pos.y < 0:
				offset = self.bottom_element.pos.y

				for element in self.elements:
					element.ui_pos = element.ui_pos[0], UIValue(element.ui_pos[1].get_pixels(self.rect.height) - offset)
					element.reposition()


class ImageElement(UIElement):
	def __init__(
			self,
			pos: tuple[UIValue, UIValue],
			size: tuple[UIValue, UIValue],
			resource_type_name: str,
			resource_name: str,
			container: Frame,
			alignment: str = "l",
	):
		self.image: Image = ResourceManager.get_resource(resource_type_name, resource_name)
		image_size = self.image.get_image().get_size()

		if size[0].value != 0 and size[1].value != 0:
			self.image: Image = self.image.scale((size[0].get_pixels(container.size.x), size[1].get_pixels(container.size.y)))
		elif size[0].value != 0:
			new_width = size[0].get_pixels(container.size.x)

			self.image: Image = self.image.scale((new_width, new_width * image_size[1] / image_size[0]))
		elif size[1].value != 0:
			new_height = size[1].get_pixels(container.size.y)

			self.image: Image = self.image.scale((new_height * image_size[0] / image_size[1], new_height))

		new_size = (
			UIValue(self.image.get_image().get_width(), True),
			UIValue(self.image.get_image().get_height(), True)
		)

		self.alignment = alignment

		if self.alignment == "l":
			# Position unchanged
			new_pos = (
				pos[0].copy(),
				pos[1].copy()
			)
		elif self.alignment == "r":
			new_pos = (
				pos[0].subtract(new_size[0], container.size.x),
				pos[1].copy()
			)
		elif self.alignment == "c":
			new_pos = (
				pos[0].subtract(new_size[0] * 0.5, container.size.x),
				pos[1].copy()
			)
		else:
			raise ValueError(f"center: `{self.alignment}` on {self.__class__.__name__} is not valid")

		super().__init__(new_pos, new_size, container)

	def draw(self, surface: pygame.Surface):
		self.image.draw(surface, self.pos)


class Button(ImageElement):
	def __init__(
			self,
			pos: tuple[UIValue, UIValue],
			size: tuple[UIValue, UIValue],
			resource_type_name: str,
			resource_name: str,
			container: Frame,
			callback: Callable[..., None],
			callback_args: tuple = (),
			text: str = "",
			text_colour="white",
			font: str = "arial",
			use_sys: bool = True,
			alignment: str = "l"
	):
		super().__init__(pos, size, resource_type_name, resource_name, container, alignment=alignment)

		self.add_action(UIActionTriggers.ON_CLICK_UP, callback, action_args=callback_args)

		self.hover_highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.hover_highlight.fill((255, 255, 255, 40))

		self.clicked_highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.clicked_highlight.fill((255, 255, 255, 70))

		self.text: Text = Text((self.pos.x + self.rect.width / 2, self.pos.y + self.rect.height * 0.5), font, int(self.size[1] * 0.7), text_colour, text, use_sys=use_sys, max_width=int(self.rect.width * 0.9), alignment=UIAlignment.CENTER)

	def reposition(self):
		super().reposition()

		self.text.pos = (self.pos.x + self.rect.width / 2, self.pos.y + self.rect.height * 0.5)
		self.text.reposition()

	def draw(self, surface: pygame.Surface):
		super().draw(surface)
		self.text.draw(surface)

		if self.clicked:
			surface.blit(self.clicked_highlight, self.pos)
		elif self.hovered:
			surface.blit(self.hover_highlight, self.pos)


class TextElement(UIElement):
	def __init__(
			self,
			pos: tuple[UIValue, UIValue],
			font_name: str,
			height: UIValue,
			colour, text: str,
			container: Frame,
			use_sys: bool = True,
			alignment: UIAlignment = UIAlignment.TOP_LEFT
	):
		self.alignment = alignment
		self.text = Text(
			(pos[0].get_pixels(container.size.x), pos[1].get_pixels(container.size.y)),
			font_name,
			int(height.get_pixels(container.size.y) * 1.2),
			colour,
			text,
			use_sys=use_sys,
			alignment=alignment
		)

		super().__init__(
			(
				UIValue(self.text.text_rect.x).add(pos[0], container.size[0]),
				UIValue(self.text.text_rect.y).add(pos[1], container.size[1])
			), (
				UIValue(self.text.text_rect.width), UIValue(self.text.text_rect.height)
			), container)

	def reposition(self):
		super().reposition()

		# Todo: Set text position
		# self.pos is topleft? While text.pos depends on alignment
		# Find a way to work around that...

		rect = self.rect.copy()
		logging.debug(f"Offset: {self.text.text}: {self.container_offset}")
		UIAlignment.set_rect(rect, self.alignment, self.pos)

		self.text.pos = UIAlignment.get_pos(self.alignment, rect)
		logging.debug(f"Before: {self.text.text}: {self.text.pos}")
		self.text.reposition()
		logging.debug(f"After: {self.text.text}: {self.text.pos}")

	# self._pos.update(self.text.text_rect.topleft)
	# self.ui_pos = (
	# 	UIValue(self.text.text_rect.x).add(self.ui_pos[0], self.container_size[0]),
	# 	UIValue(self.text.text_rect.y).add(self.ui_pos[1], self.container_size[1])
	# )

	def set_text(self, new_text: str):
		self.text.set_text(new_text)

		self._size = pygame.Vector2(self.text.text_rect.size)
		self.ui_size = (
			UIValue(self.size[0]),
			UIValue(self.size[1])
		)

		self.rect.size = self.text.text_rect.size

		self.reposition()

	def draw(self, surface: pygame.Surface):
		self.text.draw(surface)


class TextSelectionMenu(Frame):
	def __init__(
			self,
			pos: tuple[UIValue, UIValue],
			size: tuple[UIValue, UIValue],
			image_resource_type_name: str,
			options: list,
			container: Frame
	):
		super().__init__(pos, size, container=container, bg_colour=(0, 0, 0, 150))

		self.options = options

		self.index: int = 0
		self.current_option = self.options[self.index]

		self.text: Optional[TextElement] = None

		self.add_element(Button((UIValue(0, False), UIValue(0, False)), (UIValue(0, False), UIValue(1, False)), image_resource_type_name, "left", self, self._change_option, callback_args=(-1,)))
		self.add_element(Button((UIValue(1, False), UIValue(0, False)), (UIValue(0, False), UIValue(1, False)), image_resource_type_name, "right", self, self._change_option, callback_args=(1,), alignment="r"))

		self.text = TextElement((UIValue(0.5, False), UIValue(0.5, False)), "arial", UIValue(0.7, False), (255, 255, 255), self.current_option, self, alignment=UIAlignment.CENTER)
		self.add_element(self.text)

	def _change_option(self, direction):
		self.index += direction

		if self.index < 0:
			self.index = len(self.options) - 1
		elif len(self.options) <= self.index:
			self.index = 0

		self.current_option = self.options[self.index]

		self.text.set_text(self.current_option)


class ProgressBar(Frame):
	def __init__(
			self,
			pos: tuple[UIValue, UIValue],
			size: tuple[UIValue, UIValue],
			starting_fill: float,
			border_size: UIValue,
			bar_colour: tuple | str,
			background_colour: tuple | str,
			container: Frame
	):
		super().__init__(pos, size, container=container, bg_colour=background_colour)

		self.border_size = border_size

		self.fill_percent = starting_fill

		self.bar_colour = bar_colour

	def set_fill_percent(self, new_fill_percent: float):
		self.fill_percent = new_fill_percent

	def draw(self, surface: pygame.Surface):
		super().draw(surface)

		fill_rect = pygame.Rect(
			self.pos.x + self.border_size.get_pixels(self.size[0]),
			self.pos.y + self.border_size.get_pixels(self.size[1]),
			(self.size.x - self.border_size.get_pixels(self.size[0]) * 2) * self.fill_percent,
			self.size.y - self.border_size.get_pixels(self.size[1]) * 2
		)

		pygame.draw.rect(surface, self.bar_colour, fill_rect)
