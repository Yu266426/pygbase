import pygame

from . import Common
from .camera import Camera
from .inputs import InputManager


class ControlledScreen:
	def __init__(self, pos: tuple[int | float, int | float] = (0, 0), keep_in: tuple | None = None):
		self._camera: Camera = Camera(pos)
		self._prev_target: pygame.Vector2 = self._camera.pos.copy()

		self._mouse_pos: pygame.Vector2 = pygame.Vector2(pygame.mouse.get_pos())
		self._prev_mouse_pos: pygame.Vector2 = self._mouse_pos.copy()

		self._world_mouse_pos: pygame.Vector2 = self._mouse_pos.copy()

		self.keep_in = keep_in

	@property
	def camera(self):
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
		if not InputManager.get_modifiers(pygame.KMOD_LCTRL):
			x_input = InputManager.get_key_pressed(pygame.K_d) - InputManager.get_key_pressed(pygame.K_a)
			y_input = InputManager.get_key_pressed(pygame.K_s) - InputManager.get_key_pressed(pygame.K_w)

			self._camera.set_pos(self._camera.pos + pygame.Vector2(x_input, y_input) * speed * delta)

		self._handle_bounds()

	def update(self, delta):
		self._mouse_update()
		self._keyboard_control(delta)
		self._mouse_control()

	@property
	def world_mouse_pos(self):
		return self._world_mouse_pos
