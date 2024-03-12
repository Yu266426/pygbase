import enum

import pygame


class UIActionTriggers(enum.Enum):
	ON_CLICK_DOWN = enum.auto()
	ON_CLICK_UP = enum.auto()
	ON_CLICK_HOLD = enum.auto()

	ON_HOVER_ENTER = enum.auto()
	ON_HOVER_EXIT = enum.auto()
	ON_HOVER_TIME = enum.auto()

	ON_SCROLL_Y = enum.auto()


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
	def set_rect(cls, rect: pygame.Rect | pygame.FRect, alignment: "UIAlignment", pos: tuple | pygame.Vector2):
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


class UIValue:
	def __init__(self, value: float, is_pixels: bool = True):
		self.is_pixels = is_pixels

		# if not self.is_pixels:
		# 	if not (0 <= value <= 1):
		# 		raise ValueError("Percent value has to be between 0 and 1")

		self._value = value

	@property
	def value(self):
		return self._value

	def get_pixels(self, container_size: float):
		if self.is_pixels:
			return self._value
		else:
			return container_size * self._value

	def get_percent(self, container_size: float):
		if self.is_pixels:
			return self._value / container_size
		else:
			return self._value

	def add(self, other: "UIValue", container_size: float) -> "UIValue":
		if self.is_pixels == other.is_pixels:
			return UIValue(self._value + other._value, self.is_pixels)
		else:
			if self.is_pixels:
				return UIValue(self._value + other.get_pixels(container_size), True)
			else:
				return UIValue(self._value + other.get_percent(container_size), False)

	def subtract(self, other: "UIValue", container_size: float) -> "UIValue":
		if self.is_pixels == other.is_pixels:
			return UIValue(self._value - other._value, self.is_pixels)
		else:
			if self.is_pixels:
				return UIValue(self._value - other.get_pixels(container_size), True)
			else:
				return UIValue(self._value - other.get_percent(container_size), False)

	def __mul__(self, other):
		if isinstance(other, float):
			return UIValue(self._value * other, self.is_pixels)
		elif isinstance(other, UIValue):
			raise NotImplementedError()
		else:
			raise TypeError(f"unsupported operand type(s) for *: 'UIValue' and '{type(other)}'")

	def copy(self) -> "UIValue":
		return UIValue(self._value, self.is_pixels)

# def __add__(self, other: "UIValue"):
# 	if not isinstance(other, UIValue):
# 		raise TypeError(f"unsupported operand type(s) for +: 'UIValue' and '{type(other)}'")
#
# 	if self.is_pixels != other.is_pixels:
# 		raise TypeError(f"Can only add UIValues of type {'pixels' if self.is_pixels else 'percent'}")
#
# 	self.value += other.value
#
# def __sub__(self, other: "UIValue"):
# 	if not isinstance(other, UIValue):
# 		raise TypeError(f"unsupported operand type(s) for -: 'UIValue' and '{type(other)}'")
#
# 	if self.is_pixels != other.is_pixels:
# 		raise TypeError(f"Can only subtract UIValues of type {'pixels' if self.is_pixels else 'percent'}")
#
# 	self.value -= other.value
