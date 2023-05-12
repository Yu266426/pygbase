import logging
from typing import Optional, Callable

import pygame

from .enums import UIActionTriggers
from .. import Common
from ..graphics.image import Image
from ..inputs import InputManager
from ..resources import ResourceManager
from ..ui.text import Text


class UIElement:
	def __init__(self, percent_pos: tuple[float, float], percent_size: tuple[float, float], container: Optional["Frame"]):
		self.container = container

		# Percent size of container
		self.percent_pos: tuple[float, float] = percent_pos
		self.percent_size: tuple[float, float] = percent_size

		self._validate_init_values()

		if container is None:
			frame_size = Common.get_value("screen_width"), Common.get_value("screen_height")
			container_offset = (0, 0)
		else:
			frame_size = container.size
			container_offset = container.rect.topleft

		self._pos: pygame.Vector2 = pygame.Vector2(
			frame_size[0] * self.percent_pos[0],
			frame_size[1] * self.percent_pos[1]
		)
		self._size: pygame.Vector2 = pygame.Vector2(
			frame_size[0] * self.percent_size[0],
			frame_size[1] * self.percent_size[1]
		)

		self._rect: pygame.Rect = pygame.Rect(self._pos + container_offset, self.size)

		self.time = 0
		self.hovered = False

		self._actions: dict[UIActionTriggers, list[tuple[Callable[..., None], tuple]]] = {trigger: [] for trigger in UIActionTriggers}

	def _validate_init_values(self):
		# Validate ranges
		if not (0 <= self.percent_pos[0] <= 1):
			logging.error(f"Percent pos x: {self.percent_pos[0]} is not in range")
			raise ValueError(f"Percent pos x: {self.percent_pos[0]} is not in range")
		if not (0 <= self.percent_pos[1] <= 1):
			logging.error(f"Percent pos y: {self.percent_pos[1]} is not in range")
			raise ValueError(f"Percent pos y: {self.percent_pos[1]} is not in range")

		if not (0 < self.percent_size[0] <= 1):
			logging.error(f"Percent size width: {self.percent_size[0]} is not in range")
			raise ValueError(f"Percent size width: {self.percent_size[0]} is not in range")
		if not (0 < self.percent_size[1] <= 1):
			logging.error(f"Percent size height: {self.percent_size[1]} is not in range")
			raise ValueError(f"Percent size height: {self.percent_size[1]} is not in range")

	@property
	def pos(self) -> pygame.Vector2:
		return self._pos

	@property
	def size(self) -> pygame.Vector2:
		return self._size

	@property
	def rect(self) -> pygame.Rect:
		return self._rect

	def reposition(self):
		self._pos.update(
			self.container.size[0] * self.percent_pos[0],
			self.container.size[1] * self.percent_pos[1]
		)
		self._size.update(
			self.container.size[0] * self.percent_size[0],
			self.container.size[1] * self.percent_size[1]
		)

		self._rect.topleft = self.pos + self.container.rect.topleft
		self._rect.size = self.size

	def add_action(self, trigger: UIActionTriggers, action: Callable[..., None], action_args: tuple = ()) -> "UIElement":
		self._actions[trigger].append((action, action_args))
		return self

	def _perform_action(self, trigger: UIActionTriggers):
		for action in self._actions[trigger]:
			action[0](*action[1])

	def update(self, delta: float):
		self.time += delta

		if self._rect.collidepoint(pygame.mouse.get_pos()):
			if not self.hovered:
				self.hovered = True
				self._perform_action(UIActionTriggers.ON_HOVER_ENTER)

			if InputManager.mouse_down[0]:
				self._perform_action(UIActionTriggers.ON_CLICK_DOWN)
			if InputManager.mouse_up[0]:
				self._perform_action(UIActionTriggers.ON_CLICK_UP)
		else:
			if self.hovered:
				self.hovered = False

				self._perform_action(UIActionTriggers.ON_HOVER_EXIT)

	def draw(self, screen: pygame.Surface):
		pass


class Frame(UIElement):
	def __init__(self, percent_pos: tuple[float, float], percent_size: tuple[float, float], container: Optional["Frame"] = None, bg_colour=None):
		super().__init__(percent_pos, percent_size, container)

		self.active = True

		self.bg_colour = bg_colour
		self.bg = None

		if self.bg_colour is not None:
			self.bg = pygame.Surface(self._size, flags=pygame.SRCALPHA)
			self.bg.fill(self.bg_colour)

		self.elements: list[UIElement] = []

	def reposition(self):
		super().reposition()

		for element in self.elements:
			element.reposition()

	def add_element(self, element: UIElement, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> UIElement:
		if len(self.elements) > 0:
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

		element.reposition()

		out_of_bounds = False

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

	def draw(self, screen: pygame.Surface):
		if self.active:
			if self.bg is not None:
				screen.blit(self.bg, self._rect)

			for element in self.elements:
				element.draw(screen)


class ImageElement(UIElement):
	def __init__(
			self,
			percent_pos: tuple[float, float],
			percent_size: tuple[float, float],
			resource_type: int,
			resource_name: str,
			container: Frame,
			alignment: str = "l",
	):
		self.image: Image = ResourceManager.get_resource(resource_type, resource_name)
		image_size = self.image.get_image().get_size()

		if percent_size[0] != 0 and percent_size[1] != 0:
			self.image: Image = self.image.scale((container._size.x * percent_size[0], container._size.y * percent_size[1]))
		elif percent_size[0] != 0:
			new_width = container._size[0] * percent_size[0]

			self.image: Image = self.image.scale((new_width, new_width * image_size[1] / image_size[0]))
		elif percent_size[1] != 0:
			new_height = container._size[1] * percent_size[1]

			self.image: Image = self.image.scale((new_height * image_size[0] / image_size[1], new_height))

		new_percent_size = (
			self.image.get_image().get_width() / container._size[0],
			self.image.get_image().get_height() / container._size[1]
		)

		self.alignment = alignment
		new_percent_pos = percent_pos
		if self.alignment == "l":
			# Position unchanged
			pass
		elif self.alignment == "r":
			new_percent_pos = (
				percent_pos[0] - new_percent_size[0],
				percent_pos[1]
			)
		elif self.alignment == "c":
			new_percent_pos = (
				percent_pos[0] - new_percent_size[0] / 2,
				percent_pos[1]
			)
		else:
			raise ValueError(f"center: `{self.alignment}` on {self.__class__.__name__} is not valid")

		super().__init__(new_percent_pos, new_percent_size, container)

	def draw(self, screen: pygame.Surface):
		self.image.draw(screen, self._rect)


class Button(ImageElement):
	def __init__(
			self,
			percent_pos: tuple[float, float],
			percent_size: tuple[float, float],
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
		super().__init__(percent_pos, percent_size, resource_type, resource_name, container, alignment=alignment)

		self.add_action(UIActionTriggers.ON_CLICK_UP, callback, action_args=callback_args)

		self.highlight = pygame.Surface(self.image.get_image().get_size()).convert_alpha()
		self.highlight.fill((255, 255, 255, 40))

		self.text: Text = Text((self.rect.centerx, self.rect.top + self.rect.height * 0.2), font, self.size[1] * 0.7, text_colour, text, use_sys=True)

	def reposition(self):
		super().reposition()

		self.text.pos = (self.rect.centerx, self.rect.top + self.rect.height * 0.2)

	def draw(self, screen: pygame.Surface):
		super().draw(screen)
		self.text.draw(screen, "c")

		if self.hovered:
			screen.blit(self.highlight, self.rect)


class TextElement(UIElement):
	def __init__(
			self,
			percent_pos: tuple[float, float],
			font_name: str,
			percent_height: float,
			colour, text: str,
			container: Frame,
			centered=False,
			use_sys=True
	):
		self.text = Text(
			percent_pos * container.size,
			font_name,
			percent_height * container.size.y * 1.25,
			colour,
			text,
			use_sys=use_sys
		)

		super().__init__(percent_pos, (self.text.rendered_text[1].width / container.size[0], percent_height), container)

		self.centered = centered

	def reposition(self):
		super().reposition()

		self.text.pos = self.rect.topleft

	def set_text(self, new_text: str):
		self.text.set_text(new_text)

		self._size = self.text.rendered_text[1].size
		self.percent_size = (
			self.size[0] / self.container.size[0],
			self.size[1] / self.container.size[1]
		)

		self.rect.size = self.text.rendered_text[0].get_size()

	def draw(self, screen: pygame.Surface):
		render_surface = pygame.Surface(self.text.rendered_text[1].size).convert_alpha()
		render_surface.fill((0, 0, 0, 0))
		self.text.draw(render_surface, pos=(0, 0))
		self._rect.width = render_surface.get_width()

		offset = 0
		if self.centered:
			offset = self._rect.width / 2
		screen.blit(render_surface, (self._rect.x - offset, self._rect.y))


class TextSelectionMenu(Frame):
	def __init__(
			self,
			percent_pos: tuple[float, float],
			percent_size: tuple[float, float],
			image_resource_type: int,
			options: list,
			container: Optional[Frame] = None
	):
		super().__init__(percent_pos, percent_size, container=container, bg_colour=(0, 0, 0, 150))

		self.image_resource_type = image_resource_type

		self.options = options

		self.index: int = 0
		self.current_option = self.options[self.index]

		self.text: Optional[TextElement] = None

		self.add_element(Button((0, 0), (0, 1), self.image_resource_type, "left", self, self._change_option, callback_args=(-1,)))
		self.add_element(Button((1, 0), (0, 1), self.image_resource_type, "right", self, self._change_option, callback_args=(1,), alignment="r"))

		self.text = TextElement((0.5, 0.15), "arial", 0.7, (255, 255, 255), self.current_option, self, centered=True)
		self.add_element(self.text)

	def _change_option(self, direction):
		self.index += direction

		if self.index < 0:
			self.index = len(self.options) - 1
		elif len(self.options) <= self.index:
			self.index = 0

		self.current_option = self.options[self.index]

		self.text.set_text(self.current_option)
