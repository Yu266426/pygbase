import random

import pygame

from .common import Common
from .inputs import InputManager


class Camera:
	def __init__(self, pos: pygame.typing.Point = (0, 0), shake_amount: float = 2):
		self.pos: pygame.Vector2 = pygame.Vector2(pos)

		self._shake_amount: float = shake_amount
		self._shake_time: float = 0

		self._current_shake_offset = pygame.Vector2()

	def copy(self):
		new_camera = Camera(self.pos, self._shake_amount)
		new_camera._shake_time = self._shake_time
		new_camera._current_shake_offset = self._current_shake_offset
		return new_camera

	def shake_screen(self, time: float):
		self._shake_time = max(self._shake_time, time)

	def tick(self, delta: float):
		self._shake_time = max(self._shake_time - delta, 0)

		if self._shake_time > 0.01:
			shake_amount = self._shake_amount + self._shake_time  # More shake the longer it is
			self._current_shake_offset.update(
				random.uniform(-shake_amount, shake_amount),
				random.uniform(-shake_amount, shake_amount)
			)

	def set_pos(self, target: pygame.Vector2):
		self.pos.update(target.copy())

	def lerp_to_target(self, target: pygame.typing.Point, amount: float):
		amount = max(0.0, min(amount, 1.0))
		if self.pos.distance_to(target) < 0.1:  # Correct any minor position error
			self.pos.update(target)
		else:
			self.pos.update(self.pos.lerp(target, amount))

	def screen_to_world(self, pos: pygame.typing.Point) -> pygame.Vector2:
		return pygame.Vector2(pos[0] + self.pos.x + self._current_shake_offset.x, pos[1] + self.pos.y + self._current_shake_offset.y)

	def world_to_screen(self, pos: pygame.typing.Point) -> tuple[int, int]:
		return round(pos[0] - self.pos.x - self._current_shake_offset.x), round(pos[1] - self.pos.y - self._current_shake_offset.y)

	def world_to_screen_rect[RectType](self, rect: RectType) -> RectType:
		new_rect = rect.copy()
		new_rect.topleft = self.world_to_screen(new_rect.topleft)
		return new_rect


class CameraController:
	def __init__(self, pos: pygame.typing.Point = (0, 0), keep_in: tuple | None = None):
		self._camera: Camera = Camera(pos)
		self._prev_target: pygame.Vector2 = self._camera.pos.copy()

		self._mouse_pos: pygame.Vector2 = pygame.Vector2(pygame.mouse.get_pos())
		self._prev_mouse_pos: pygame.Vector2 = self._mouse_pos.copy()

		self._world_mouse_pos: pygame.Vector2 = self._mouse_pos.copy()

		self.keep_in = keep_in

	@property
	def camera(self) -> Camera:
		return self._camera

	def _handle_bounds(self):
		screen_width = Common.get_value("screen_width")
		screen_height = Common.get_value("screen_height")
		if self.keep_in is not None:
			if self.keep_in[2] - self.keep_in[0] < screen_width:
				if self.keep_in[0] < self._camera.pos.x:
					self._camera.pos.x = self.keep_in[0]
				if self._camera.pos.x + screen_width < self.keep_in[2]:
					self._camera.pos.x = self.keep_in[2] - screen_width
			else:
				if self._camera.pos.x < self.keep_in[0] - 30:
					self._camera.pos.x = self.keep_in[0] - 30
				if self.keep_in[2] + 30 < self._camera.pos.x + screen_width:
					self._camera.pos.x = self.keep_in[2] - screen_width + 30

			if self.keep_in[3] - self.keep_in[1] < screen_height:
				if self.keep_in[1] < self._camera.pos.y:
					self._camera.pos.y = self.keep_in[1]
				if self._camera.pos.y + screen_height < self.keep_in[3]:
					self._camera.pos.y = self.keep_in[3] - screen_height
			else:
				if self._camera.pos.y < self.keep_in[1] - 30:
					self._camera.pos.y = self.keep_in[1] - 30
				if self.keep_in[3] + 30 < self._camera.pos.y + screen_height:
					self._camera.pos.y = self.keep_in[3] - screen_height + 30

	def _mouse_update(self):
		self._mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

		self._world_mouse_pos = self._camera.screen_to_world(self._mouse_pos)

	def _mouse_control(self, mouse_button: int = 1):
		if InputManager.get_mouse_just_pressed(mouse_button):
			self._prev_mouse_pos = self._mouse_pos.copy()
			self._prev_target = self._camera.pos.copy()
		if InputManager.get_mouse_pressed(mouse_button):
			self._camera.set_pos(self._prev_target + (self._prev_mouse_pos - self._mouse_pos))

		self._handle_bounds()

	def _keyboard_control(self, delta: float, speed: float = 600):
		if not InputManager.check_modifiers(pygame.KMOD_LCTRL):
			x_input = InputManager.get_key_pressed(pygame.K_d) - InputManager.get_key_pressed(pygame.K_a)
			y_input = InputManager.get_key_pressed(pygame.K_s) - InputManager.get_key_pressed(pygame.K_w)

			self._camera.set_pos(self._camera.pos + pygame.Vector2(x_input, y_input) * speed * delta)

		self._handle_bounds()

	def update(self, delta):
		self._mouse_update()
		self._keyboard_control(delta)
		self._mouse_control()

	@property
	def world_mouse_pos(self) -> pygame.Vector2:
		return self._world_mouse_pos
