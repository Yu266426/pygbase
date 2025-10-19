import enum

import pygame

from ..debug import Debug


class UIAlignment(enum.Enum):
	TOP_LEFT = enum.auto()
	TOP_MID = enum.auto()
	TOP_RIGHT = enum.auto()

	MID_LEFT = enum.auto()
	CENTER = enum.auto()
	MID_RIGHT = enum.auto()

	BOTTOM_LEFT = enum.auto()
	BOTTOM_MID = enum.auto()
	BOTTOM_RIGHT = enum.auto()

	@classmethod
	def set_rect(cls, rect: pygame.Rect | pygame.FRect, alignment: "UIAlignment", pos: pygame.typing.Point):
		if alignment == cls.TOP_LEFT:
			rect.topleft = pos
		elif alignment == cls.TOP_MID:
			rect.midtop = pos
		elif alignment == cls.TOP_RIGHT:
			rect.topright = pos

		elif alignment == cls.MID_LEFT:
			rect.midleft = pos
		elif alignment == cls.CENTER:
			rect.center = pos
		elif alignment == cls.MID_RIGHT:
			rect.midright = pos

		elif alignment == cls.BOTTOM_LEFT:
			rect.bottomleft = pos
		elif alignment == cls.BOTTOM_MID:
			rect.midbottom = pos
		elif alignment == cls.BOTTOM_RIGHT:
			rect.bottomright = pos

	@classmethod
	def get_pos(cls, alignment: "UIAlignment", rect: pygame.Rect | pygame.FRect) -> tuple[float, float]:
		if alignment == cls.TOP_LEFT:
			return rect.topleft
		elif alignment == cls.TOP_MID:
			return rect.midtop
		elif alignment == cls.TOP_RIGHT:
			return rect.topright

		elif alignment == cls.MID_LEFT:
			return rect.midleft
		elif alignment == cls.CENTER:
			return rect.center
		elif alignment == cls.MID_RIGHT:
			return rect.midright

		elif alignment == cls.BOTTOM_LEFT:
			return rect.bottomleft
		elif alignment == cls.BOTTOM_MID:
			return rect.midbottom
		elif alignment == cls.BOTTOM_RIGHT:
			return rect.bottomright

		raise RuntimeError(f"Unknown alignment: {alignment}")


class TextOverflowBehaviour(enum.Enum):
	WRAP = enum.auto()
	SHRINK = enum.auto()


class RawText:
	def __init__(
			self,
			pos: tuple | pygame.Vector2,
			font_name: str,
			size: int,
			colour: pygame.Color | str | tuple,
			text: str = "",
			use_sys: bool = False,
			max_width: int = 0,
			overflow_behaviour: TextOverflowBehaviour = TextOverflowBehaviour.SHRINK,
			alignment: UIAlignment = UIAlignment.TOP_LEFT,
	):
		if use_sys:
			self.font = pygame.font.SysFont(font_name, size)
		else:
			self.font = pygame.font.Font(font_name, size)

		self.text = text

		self.colour = colour

		self.pos: pygame.Vector2 = pygame.Vector2(pos)

		self.alignment = alignment
		self.overflow_behaviour = overflow_behaviour
		self.max_width = max_width

		self.rendered_text: pygame.Surface
		self.text_rect: pygame.Rect
		self._render_text()

	def set_text(self, text: str):
		self.text = text
		self._render_text()

	def _render_text(self):
		if self.overflow_behaviour == TextOverflowBehaviour.WRAP:
			self.rendered_text = self.font.render(
				self.text, True, self.colour, wraplength=self.max_width
			).convert_alpha()
		elif self.overflow_behaviour == TextOverflowBehaviour.SHRINK:
			self.rendered_text = self.font.render(self.text, True, self.colour).convert_alpha()

			# Scale down to fit surface
			if self.max_width != 0:
				if self.rendered_text.get_width() > self.max_width:
					ratio = self.max_width / self.rendered_text.get_width()
					self.rendered_text = pygame.transform.smoothscale_by(self.rendered_text, ratio)

		self.reposition()

	def reposition(self):
		self.text_rect = self.rendered_text.get_rect()
		UIAlignment.set_rect(self.text_rect, self.alignment, self.pos)

	def draw(self, surface: pygame.Surface) -> None:
		surface.blit(self.rendered_text, self.text_rect)
		Debug.draw_rect(self.text_rect, "yellow")
