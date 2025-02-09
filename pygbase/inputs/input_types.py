import enum


class InputTypes(enum.Enum):
	KEY = enum.auto()
	MOUSE = enum.auto()
	CONTROLLER = enum.auto()


class MouseInput(enum.Enum):
	LEFT_CLICK = enum.auto()
	MIDDLE_CLICK = enum.auto()
	RIGHT_CLICK = enum.auto()


class ControllerTypes(enum.Enum):
	DEFAULT = enum.auto()  # Xbox 360
	SWITCH_PRO = enum.auto()


class ControllerInput(enum.Enum):
	LEFT_JOYSTICK_X = enum.auto()
	LEFT_JOYSTICK_Y = enum.auto()
	RIGHT_JOYSTICK_X = enum.auto()
	RIGHT_JOYSTICK_Y = enum.auto()

	LEFT_SHOULDER = enum.auto()
	LEFT_TRIGGER = enum.auto()
	RIGHT_SHOULDER = enum.auto()
	RIGHT_TRIGGER = enum.auto()

	DPAD_UP = enum.auto()
	DPAD_DOWN = enum.auto()
	DPAD_LEFT = enum.auto()
	DPAD_RIGHT = enum.auto()

	BUTTON_UP = enum.auto()
	BUTTON_DOWN = enum.auto()
	BUTTON_LEFT = enum.auto()
	BUTTON_RIGHT = enum.auto()

	BUTTON_START = enum.auto()
	BUTTON_SELECT = enum.auto()
