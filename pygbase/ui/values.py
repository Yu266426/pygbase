import enum
from dataclasses import dataclass

import pygame

EPSILON = 0.0001


class Layout(enum.Enum):
	LEFT_TO_RIGHT = enum.auto()
	TOP_TO_BOTTOM = enum.auto()


class XAlign(enum.Enum):
	LEFT = enum.auto()
	CENTER = enum.auto()
	RIGHT = enum.auto()


class YAlign(enum.Enum):
	TOP = enum.auto()
	CENTER = enum.auto()
	BOTTOM = enum.auto()


@dataclass
class Padding:
	left: float = 0
	right: float = 0
	top: float = 0
	bottom: float = 0

	@classmethod
	def all(cls, value: float):
		return cls(value, value, value, value)


@dataclass
class Fit:
	min: float = 0
	max: float = float("inf")


@dataclass
class Grow:
	weight: float = 1
	min: float = 0
	max: float = float("inf")


class UIActionTriggers(enum.Enum):
	ON_CLICK_DOWN = enum.auto()
	ON_CLICK_UP = enum.auto()
	ON_CLICK_HOLD = enum.auto()

	ON_HOVER_ENTER = enum.auto()
	ON_HOVER_EXIT = enum.auto()
	ON_HOVER_TIME = enum.auto()

	ON_SCROLL_Y = enum.auto()
	ON_SCROLL_X = enum.auto()
