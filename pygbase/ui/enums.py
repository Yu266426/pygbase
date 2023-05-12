import enum


class UIActionTriggers(enum.Enum):
	ON_CLICK_DOWN = enum.auto()
	ON_CLICK_UP = enum.auto()
	ON_CLICK_HOLD = enum.auto()

	ON_HOVER_ENTER = enum.auto()
	ON_HOVER_EXIT = enum.auto()
	ON_HOVER_TIME = enum.auto()


class UIAnchors(enum.Enum):
	TOP_LEFT = enum.auto()
	TOP_MID = enum.auto()
	TOP_RIGHT = enum.auto()

	MID_LEFT = enum.auto()
	CENTER = enum.auto()
	MID_RIGHT = enum.auto()

	BOTTOM_LEFT = enum.auto()
	BOTTOM_MID = enum.auto()
	BOTTOM_RIGHT = enum.auto()
