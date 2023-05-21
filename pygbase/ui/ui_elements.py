import logging
from typing import Optional, Callable

import pygame

from .ui_element import UIElement, UIElementType
from .values import UIActionTriggers, UIValue
from ..graphics.image import Image
from ..inputs import InputManager
from ..resources import ResourceManager
from ..ui.text import Text


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

		self.elements: list[UIElement] = []

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

		out_of_bounds: bool = False

		# If element does not go out of frame, add it to the frame
		if 0 <= element._pos[0] and element._pos[0] + element.size[0] <= self._size[0]:
			if 0 <= element._pos[1] and element._pos[1] + element.size[1] <= self._size[1]:
				self.elements.append(element)
			else:
				out_of_bounds = True
		else:
			out_of_bounds = True

		if out_of_bounds:
			logging.warning(f"Element <{type(element).__name__}>(size: {element.size}, pos: {element._pos}) is not contained within frame (size: {self._size})")

		# return self
		return element

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
			resource_type: int,
			resource_name: str,
			container: Frame,
			alignment: str = "l",
	):
		self.image: Image = ResourceManager.get_resource(resource_type, resource_name)
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
			resource_type: int,
			resource_name: str,
			container: Frame,
			callback: Callable[..., None],
			callback_args: tuple = (),
			text: str = "",
			text_colour="white",
			font: str = "arial",
			alignment: str = "l"
	):
		super().__init__(pos, size, resource_type, resource_name, container, alignment=alignment)

		self.add_action(UIActionTriggers.ON_CLICK_UP, callback, action_args=callback_args)

		self.hover_highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.hover_highlight.fill((255, 255, 255, 40))

		self.clicked_highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.clicked_highlight.fill((255, 255, 255, 70))

		self.text: Text = Text((self.pos.x + self.rect.width / 2, self.pos.y + self.rect.height * 0.2), font, self.size[1] * 0.7, text_colour, text, use_sys=True)

	def reposition(self):
		super().reposition()

		self.text.pos = (self.pos.x + self.rect.width / 2, self.pos.y + self.rect.height * 0.2)

	def draw(self, surface: pygame.Surface):
		super().draw(surface)
		self.text.draw(surface, "c")

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
			centered=False,
			use_sys=True
	):
		self.text = Text(
			(pos[0].get_pixels(container.size.x), pos[1].get_pixels(container.size.y)),
			font_name,
			height.get_pixels(container.size.y) * 1.25,
			colour,
			text,
			use_sys=use_sys
		)

		super().__init__(pos, (UIValue(self.text.rendered_text[1].width, True), height), container)

		self.centered = centered

	def reposition(self):
		super().reposition()

		self.text.pos = self.rect.topleft

	def set_text(self, new_text: str):
		self.text.set_text(new_text)

		self._size = pygame.Vector2(self.text.rendered_text[1].size)
		self.ui_size = (
			UIValue(self.size[0], True),
			UIValue(self.size[1], True)
		)

		self.rect.size = self.text.rendered_text[0].get_size()

	def draw(self, surface: pygame.Surface):
		render_surface = pygame.Surface(self.text.rendered_text[1].size).convert_alpha()
		render_surface.fill((0, 0, 0, 0))
		self.text.draw(render_surface, pos=(0, 0))
		self._rect.width = render_surface.get_width()

		offset = 0
		if self.centered:
			offset = self._rect.width / 2
		surface.blit(render_surface, (self.pos.x - offset, self.pos.y))


class TextSelectionMenu(Frame):
	def __init__(
			self,
			pos: tuple[UIValue, UIValue],
			size: tuple[UIValue, UIValue],
			image_resource_type: int,
			options: list,
			container: Optional[Frame] = None
	):
		super().__init__(pos, size, container=container, bg_colour=(0, 0, 0, 150))

		self.image_resource_type = image_resource_type

		self.options = options

		self.index: int = 0
		self.current_option = self.options[self.index]

		self.text: Optional[TextElement] = None

		self.add_element(Button((UIValue(0, False), UIValue(0, False)), (UIValue(0, False), UIValue(1, False)), self.image_resource_type, "left", self, self._change_option, callback_args=(-1,)))
		self.add_element(Button((UIValue(1, False), UIValue(0, False)), (UIValue(0, False), UIValue(1, False)), self.image_resource_type, "right", self, self._change_option, callback_args=(1,), alignment="r"))

		self.text = TextElement((UIValue(0.5, False), UIValue(0.15, False)), "arial", UIValue(0.7, False), (255, 255, 255), self.current_option, self, centered=True)
		self.add_element(self.text)

	def _change_option(self, direction):
		self.index += direction

		if self.index < 0:
			self.index = len(self.options) - 1
		elif len(self.options) <= self.index:
			self.index = 0

		self.current_option = self.options[self.index]

		self.text.set_text(self.current_option)
