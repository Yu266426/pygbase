import pygame.mouse

from .events import EventManager


class InputManager:
	# Keyboard
	_keys_down = [False] * 512
	_keys_pressed = [False] * 512
	_keys_up = [False] * 512

	# Mouse
	_mouse_down: list[bool, bool, bool] = [False, False, False]
	_mouse_up: list[bool, bool, bool] = [False, False, False]
	_mouse_pressed: tuple[bool, bool, bool] = (False, False, False)

	_scroll: pygame.Vector2 = pygame.Vector2()

	_mods = 0

	@classmethod
	def reset(cls):
		"""(Called by the engine)"""
		cls._mouse_down[:] = [False, False, False]
		cls._mouse_up[:] = [False, False, False]
		cls._mouse_pressed = pygame.mouse.get_pressed(3)

		cls._scroll.update(0)

		cls._keys_down[:] = [False] * 512
		cls._keys_up[:] = [False] * 512
		cls._keys_pressed = pygame.key.get_pressed()

		cls._mods = pygame.key.get_mods()

	# Getters
	@classmethod
	def get_key_pressed(cls, key_id: int):
		"""Returns if a key is held down"""
		return cls._keys_pressed[key_id]

	@classmethod
	def get_key_just_pressed(cls, key_id: int):
		return cls._keys_down[key_id]

	@classmethod
	def get_key_just_released(cls, key_id: int):
		return cls._keys_up[key_id]

	@classmethod
	def get_mouse_pressed(cls, mouse_button: int):
		if 0 <= mouse_button <= 2:
			return cls._mouse_pressed[mouse_button]
		else:
			raise ValueError("Mouse button must be between 0-2")

	@classmethod
	def get_mouse_just_pressed(cls, mouse_button: int):
		if 0 <= mouse_button <= 2:
			return cls._mouse_down[mouse_button]
		else:
			raise ValueError("Mouse button must be between 0-2")

	@classmethod
	def get_mouse_just_released(cls, mouse_button: int):
		if 0 <= mouse_button <= 2:
			return cls._mouse_up[mouse_button]
		else:
			raise ValueError("Mouse button must be between 0-2")

	@classmethod
	def get_scroll(cls):
		return cls._scroll.copy()

	@classmethod
	def get_scroll_x(cls):
		return cls._scroll.x

	@classmethod
	def get_scroll_y(cls):
		return cls._scroll.y

	@classmethod
	def check_modifiers(cls, *modifiers):
		result = True
		for modifier in modifiers:
			if not cls._mods & modifier:
				result = False
				break

		return result

	@classmethod
	def register_handlers(cls):
		"""(Called by the engine)"""
		EventManager.add_handler("all", pygame.KEYDOWN, cls._keydown_handler)
		EventManager.add_handler("all", pygame.KEYUP, cls._keyup_handler)
		EventManager.add_handler("all", pygame.MOUSEBUTTONDOWN, cls._mouse_down_handler)
		EventManager.add_handler("all", pygame.MOUSEBUTTONUP, cls._mouse_up_handler)
		EventManager.add_handler("all", pygame.MOUSEWHEEL, cls._mouse_wheel_handler)

	@classmethod
	def _keydown_handler(cls, event: pygame.event.Event):
		if event.key <= 512:
			cls._keys_down[event.key] = True

	@classmethod
	def _keyup_handler(cls, event: pygame.event.Event):
		if event.key <= 512:
			cls._keys_up[event.key] = True

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
