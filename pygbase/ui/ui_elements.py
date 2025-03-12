from typing import Callable

import pygame

from .ui_element import Frame
from .values import Fit, Grow, Layout, Padding, XAlign, YAlign, UIActionTriggers
from .. import Resources


class Text(Frame):
	ID: str = "text"

	def __init__(
			self,
			text: str,
			font_size: int,
			color: str,
			pos: tuple[float, float] = (0, 0),
			size: tuple[float | Fit | Grow, float | Fit | Grow] = (Fit(), Fit()),
			layout: Layout = Layout.LEFT_TO_RIGHT,
			padding: Padding = Padding(),
			gap: float = 0,
			x_align: XAlign = XAlign.LEFT,
			y_align: YAlign = YAlign.TOP,
			bg_color: pygame.typing.ColorLike = (0, 0, 0, 0),
	):
		super().__init__(
			pos,
			size,
			layout,
			padding,
			gap,
			x_align,
			y_align,
			bg_color,
		)

		self._text = text
		self._font_size = font_size
		self.color = color

		self.font = pygame.font.SysFont("arial", font_size)
		self._text_surface = None

		self.set_text(text)

	def set_text(self, text: str):
		self._text = text

		# Find the minimum size based on the largest word
		self._iter_min_size.x = 0
		self._iter_min_size.y = 0
		for word in text.split(" "):
			word_size = self.font.size(word)
			self._iter_min_size.x = max(self._iter_min_size.x, word_size[0])
			self._iter_min_size.y = max(self._iter_min_size.y, word_size[1])

		# Set the preferred size of the full text
		self._size.update(self.font.size(self._text))

	def _wrap_text(self):
		self._text_surface = self.font.render(self._text, True, self.color, wraplength=int(self.size.x))
		self.min_height = self._text_surface.height

		super()._wrap_text()

	def _draw_self(self, surface: pygame.Surface):
		if self._text_surface is not None:
			surface.blit(self._text_surface, self._draw_pos)


# Debug.draw_rect(self._text_surface.get_rect(topleft=self._draw_pos), "yellow", width=1)


class Image(Frame):
	ID: str = "image"

	def __init__(
			self,
			image_name: str | None = None,
			pos: tuple[float, float] = (0, 0),
			size: tuple[float | Fit | Grow, float | Fit | Grow] = (Fit(), Fit()),
			layout: Layout = Layout.LEFT_TO_RIGHT,
			padding: Padding = Padding(),
			gap: float = 0,
			x_align: XAlign = XAlign.LEFT,
			y_align: YAlign = YAlign.TOP,
			bg_color: pygame.typing.ColorLike = (0, 0, 0, 0),
	):
		super().__init__(
			pos,
			size,
			layout,
			padding,
			gap,
			x_align,
			y_align,
			bg_color,
		)

		self.image_name = image_name

		if image_name is not None:
			self._raw_image = Resources.get_resource("image", image_name).get_image()

			if self._raw_image.get_height() == 0:
				raise ValueError("Image height is zero; cannot compute aspect ratio.")
			self._aspect_ratio = self._raw_image.get_width() / self._raw_image.get_height()
			# print(self.background_color, self._aspect_ratio)

			self._image = self._raw_image.copy()
			self._size.update(self._raw_image.get_width(), self._raw_image.get_height())

	def _fix_aspect_ratio(self):
		if self.image_name is not None:
			if isinstance(self.size_settings[0], Fit):
				# print("Fixed X:", self.min_width, self.width, self._iter_min_size.x)

				self._iter_min_size.x = pygame.math.clamp(
					self.height * self._aspect_ratio, self.min_width, self._max_size.x
				)
				self.min_width = self._iter_min_size.x
				self.width = max(self.width, self.min_width)

			if isinstance(self.size_settings[1], Fit):
				# print("Fixed Y:", self.min_height, self.height, self._iter_min_size.y)

				self._iter_min_size.y = pygame.math.clamp(
					self.width / self._aspect_ratio, self._iter_min_size.y, self._max_size.y
				)
				self.min_height = self.min_height
				self.height = max(self.height, self.min_height)

	def _shrink_children_x(self):
		super()._shrink_children_x()

		# This is the last pass that runs
		self._fix_aspect_ratio()

	def _shrink_children_y(self):
		super()._shrink_children_y()

		self._fix_aspect_ratio()

	def _draw_self(self, surface: pygame.Surface):
		if self.image_name is not None and self.size != pygame.Vector2(self._image.get_size()):
			self._image = pygame.transform.scale(
				self._raw_image, (int(self.width), int(self.height))
			)
		surface.blit(self._image, self._draw_pos)


class Button(Frame):
	ID: str = "button"

	def __init__(
			self,
			callback: Callable[..., None],
			callback_args: tuple = (),
			pos: tuple[float, float] = (0, 0),
			size: tuple[float | Fit | Grow, float | Fit | Grow] = (Fit(), Fit()),
			layout: Layout = Layout.LEFT_TO_RIGHT,
			padding: Padding = Padding(),
			gap: float = 0,
			x_align: XAlign = XAlign.LEFT,
			y_align: YAlign = YAlign.TOP,
			bg_color: pygame.typing.ColorLike = (0, 0, 0, 0),
	):
		super().__init__(
			pos,
			size,
			layout,
			padding,
			gap,
			x_align,
			y_align,
			bg_color,
		)

		self.add_action(UIActionTriggers.ON_CLICK_UP, callback, action_args=callback_args)

	def _draw_overlay(self, surface: pygame.Surface):
		if self._hovered:
			surface.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)
		if self._clicked:
			surface.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)
