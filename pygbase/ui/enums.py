import enum


class UIActionTriggers(enum.Enum):
	ON_CLICK_DOWN = enum.auto()
	ON_CLICK_UP = enum.auto()
	ON_CLICK_HOLD = enum.auto()

	ON_HOVER_ENTER = enum.auto()
	ON_HOVER_EXIT = enum.auto()
	ON_HOVER_TIME = enum.auto()
