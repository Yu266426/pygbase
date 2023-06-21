import enum

import pygame

from .values import UIAnchors


class TextOverflowBehaviour(enum.Enum):
	WRAP = enum.auto()
	SHRINK = enum.auto()


class Text:
	def __init__(self, pos: tuple | pygame.Vector2, font_name: str, size: int, colour: pygame.Color | str | tuple, text: str = "", use_sys: bool = False, overflow_behaviour: TextOverflowBehaviour = TextOverflowBehaviour.SHRINK, max_width: int = 0, anchor: UIAnchors = UIAnchors.TOP_LEFT):
		if use_sys:
			self.font = pygame.font.SysFont(font_name, size)
		else:
			self.font = pygame.font.Font(font_name, size)

		self.text = text

		self.colour = colour

		self.pos = pygame.Vector2(pos)

		self.anchor = anchor
		self.overflow_behaviour = overflow_behaviour
		self.max_width = max_width

		self.rendered_text: pygame.Surface | None = None
		self.text_rect: pygame.Rect | None = None
		self._render_text()

	def set_text(self, text: str):
		self.text = text
		self._render_text()

	def _render_text(self):
		if self.overflow_behaviour == TextOverflowBehaviour.WRAP:
			self.rendered_text = self.font.render(self.text, True, self.colour, wraplength=self.max_width).convert_alpha()
		elif self.overflow_behaviour == TextOverflowBehaviour.SHRINK:
			self.rendered_text = self.font.render(self.text, True, self.colour).convert_alpha()

			if self.max_width != 0:
				if self.rendered_text.get_width() > self.max_width:
					ratio = self.max_width / self.rendered_text.get_width()
					self.rendered_text = pygame.transform.smoothscale_by(self.rendered_text, ratio)

		self.reposition()

	def reposition(self):
		self.text_rect = self.rendered_text.get_rect()
		UIAnchors.set_rect(self.text_rect, self.anchor, self.pos)

	def draw(self, surface: pygame.Surface) -> None:
		surface.blit(self.rendered_text, self.text_rect)
