import typing

import pygame

from ..events import Events
from .input_types import ControllerInput, InputTypes, MouseInput


class Input:
	# Keyboard
	_keys_down = [False] * 512
	_keys_up = [False] * 512
	_keys_pressed = [False] * 512

	# Mouse
	_mouse_down: list[bool] = [False, False, False]
	_mouse_up: list[bool] = [False, False, False]
	_mouse_pressed: list[bool, bool, bool] = [False, False, False]

	_scroll: pygame.Vector2 = pygame.Vector2()

	_mods = 0

	# Keybinds
	_keybinds: dict[str, tuple[typing.Any, InputTypes]] = {}

	# name: (neg, pos) | joystick
	_keybind_axes: dict[str, tuple[str, str] | str] = {}

	@classmethod
	def reset(cls):
		"""(Called by the engine)"""
		cls._mouse_down[:] = [False, False, False]
		cls._mouse_up[:] = [False, False, False]
		cls._mouse_pressed[:] = list(pygame.mouse.get_pressed(3))

		cls._scroll.update(0)

		cls._keys_down = pygame.key.get_just_pressed()
		cls._keys_up = pygame.key.get_just_released()
		cls._keys_pressed = pygame.key.get_pressed()

		cls._mods = pygame.key.get_mods()

	# Keybinds
	@classmethod
	def set_keybind(cls, name: str, user_input: MouseInput | ControllerInput | int | str):
		# TODO: Make multiple binds for the same input possible
		#  would require a remove_keybind too possibly
		input_type = cls._get_input_type_from_input(user_input)

		key = user_input
		if input_type == InputTypes.KEY:
			key = cls._get_key_from_input(user_input)
		elif input_type == InputTypes.MOUSE:
			key = cls._get_mouse_from_input(user_input)

		cls._keybinds[name] = (key, input_type)

	@classmethod
	def bind_axis(cls, name: str, neg_key: str, pos_key: str):
		if cls._keybind_is_joystick(neg_key) or cls._keybind_is_joystick(pos_key):
			raise ValueError(
				"`bind_axis` does not support joystick input, use `bind_axis_to_joystick` instead"
			)

		cls._keybind_axes[name] = (neg_key, pos_key)

	@classmethod
	def bind_axis_to_joystick(cls, name: str, stick_axis: str):
		if not cls._keybind_is_joystick(stick_axis):
			raise ValueError(f"Input <{stick_axis}> be joystick for `bind_axis_to_joystick`")

		cls._keybind_axes[name] = stick_axis

	@staticmethod
	def _get_input_type_from_input(
			user_input: MouseInput | ControllerInput | int | str,
	) -> InputTypes:
		# Check for mouse
		if isinstance(user_input, MouseInput):
			return InputTypes.MOUSE

		if isinstance(user_input, ControllerInput):
			return InputTypes.CONTROLLER

		# Check for key
		if isinstance(user_input, str):
			key_string = user_input
		else:
			key_string = pygame.key.name(user_input)  # Becomes "" if not a key

		try:
			pygame.key.key_code(key_string)
			return InputTypes.KEY
		except ValueError:
			# Not a key
			raise ValueError(f"Selected input <{user_input}> is not valid")

	@staticmethod
	def _get_key_from_input(key: str | int) -> int:
		if isinstance(key, str):
			key_string = key
		else:
			key_string = pygame.key.name(key)

		return pygame.key.key_code(key_string)

	@staticmethod
	def _get_mouse_from_input(key: MouseInput) -> int:
		if key == MouseInput.LEFT_CLICK:
			return 0
		elif key == MouseInput.MIDDLE_CLICK:
			return 1
		elif key == MouseInput.RIGHT_CLICK:
			return 2
		else:
			raise ValueError(f"Unknown key: `{key}`")

	@classmethod
	def _keybind_is_joystick(cls, keybind: str):
		cls._check_keybind_exists(keybind)

		return cls._keybinds[keybind][0] in (
			ControllerInput.LEFT_JOYSTICK_X,
			ControllerInput.LEFT_JOYSTICK_Y,
			ControllerInput.RIGHT_JOYSTICK_X,
			ControllerInput.RIGHT_JOYSTICK_Y,
		)

	@classmethod
	def _check_keybind_exists(cls, keybind: str):
		if keybind not in cls._keybinds:
			raise ValueError(f"Keybind: <{keybind}> not defined")

	# Getters
	# TODO: Add just_pressed, just_released, get_axis, get_vector2
	@classmethod
	def pressed(cls, keybind: str, consume: bool = False) -> float:
		cls._check_keybind_exists(keybind)

		user_input, input_type = cls._keybinds[keybind]

		if input_type == InputTypes.KEY:
			return float(cls.key_pressed(user_input, consume))
		elif input_type == InputTypes.MOUSE:
			return float(cls.mouse_pressed(user_input, consume))
		else:
			# TODO: Handle controller inputs
			raise NotImplementedError("Controllers are not supported yet")

	@classmethod
	def key_pressed(cls, key_id: int, consume: bool = False) -> bool:
		"""Returns if a key is held down"""
		val = cls._keys_pressed[key_id]

		if consume:
			cls._keys_pressed[key_id] = False

		return val

	@classmethod
	def key_just_pressed(cls, key_id: int, consume: bool = False) -> bool:
		val = cls._keys_down[key_id]

		if consume:
			cls._keys_down[key_id] = False

		return val

	@classmethod
	def key_just_released(cls, key_id: int, consume: bool = False) -> bool:
		val = cls._keys_up[key_id]

		if consume:
			cls._keys_up[key_id] = False

		return val

	@classmethod
	def mouse_pressed(cls, mouse_button: int, consume: bool = False) -> bool:
		if 0 <= mouse_button <= 2:
			val = cls._mouse_pressed[mouse_button]

			if consume:
				cls._mouse_pressed[mouse_button] = False

			return val
		else:
			raise ValueError("Mouse button must be between 0-2")

	@classmethod
	def mouse_just_pressed(cls, mouse_button: int, consume: bool = False) -> bool:
		if 0 <= mouse_button <= 2:
			val = cls._mouse_down[mouse_button]

			if consume:
				cls._mouse_down[mouse_button] = False

			return val
		else:
			raise ValueError("Mouse button must be between 0-2")

	@classmethod
	def mouse_just_released(cls, mouse_button: int, consume: bool = False) -> bool:
		if 0 <= mouse_button <= 2:
			val = cls._mouse_up[mouse_button]

			if consume:
				cls._mouse_up[mouse_button] = False

			return val
		else:
			raise ValueError("Mouse button must be between 0-2")

	@classmethod
	def mouse_scroll(cls) -> pygame.Vector2:
		return cls._scroll.copy()

	@classmethod
	def mouse_scroll_x(cls) -> float:
		return cls._scroll.x

	@classmethod
	def mouse_scroll_y(cls) -> float:
		return cls._scroll.y

	@classmethod
	def check_modifiers(cls, *modifiers: int, use_and=True) -> bool:
		if use_and:
			for modifier in modifiers:
				if not cls._mods & modifier:
					return False
			return True

		else:
			for modifiers in modifiers:
				if cls._mods & modifiers:
					return True
			return False

	@classmethod
	def register_handlers(cls):
		"""(Called by the engine)"""
		Events.add_handler("all", pygame.MOUSEBUTTONDOWN, cls._mouse_down_handler)
		Events.add_handler("all", pygame.MOUSEBUTTONUP, cls._mouse_up_handler)
		Events.add_handler("all", pygame.MOUSEWHEEL, cls._mouse_wheel_handler)

	@classmethod
	def _mouse_down_handler(cls, event: pygame.event.Event):
		button = event.button - 1
		if button <= 2:
			cls._mouse_down[button] = True

	@classmethod
	def _mouse_up_handler(cls, event: pygame.event.Event):
		button = event.button - 1
		if button <= 2:
			cls._mouse_up[button] = True

	@classmethod
	def _mouse_wheel_handler(cls, event: pygame.event.Event):
		wheel_x = event.precise_x
		wheel_y = event.precise_y

		cls._scroll.x = wheel_x
		cls._scroll.y = wheel_y
