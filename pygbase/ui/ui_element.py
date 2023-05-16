import logging
from typing import Optional, Callable, TypeVar, TYPE_CHECKING

import pygame

from .values import UIActionTriggers, UIValue
from ..common import Common
from ..inputs import InputManager

if TYPE_CHECKING:
	from .ui_elements import Frame


class UIElement:
	def __init__(self, pos: tuple[UIValue, UIValue], size: tuple[UIValue, UIValue], container: Optional["Frame"]):
		# UI data
		self.container = container
		self._update_container_properties()

		self.ui_pos: tuple[UIValue, UIValue] = pos
		self.ui_size: tuple[UIValue, UIValue] = size

		self._pos = pygame.Vector2(
			self.ui_pos[0].get_pixels(self.container_size[0]),
			self.ui_pos[1].get_pixels(self.container_size[1])
		)
		self._size: pygame.Vector2 = pygame.Vector2(
			self.ui_size[0].get_pixels(self.container_size[0]),
			self.ui_size[1].get_pixels(self.container_size[1])
		)

		self._rect: pygame.Rect = pygame.Rect(self._pos + self.container_offset, self.size)

		# Actions data
		self.time = 0
		self.timed_actions: dict[int, list[UIActionTriggers]] = {}  # TODO: Use in some way?

		self.hovered = False
		self.clicked = False

		self._actions: dict[UIActionTriggers, list[tuple[Callable[..., None], tuple]]] = {trigger: [] for trigger in UIActionTriggers}  # TODO: Change to have list of preset actions. Callables would be an action with input of a Callable

	def _update_container_properties(self):
		if self.container is None:
			self.container_size = Common.get_value("screen_width"), Common.get_value("screen_height")
			self.container_offset = (0, 0)
		else:
			self.container_size = self.container.size
			self.container_offset = self.container.rect.topleft

	@property
	def pos(self) -> pygame.Vector2:
		return self._pos

	@property
	def size(self) -> pygame.Vector2:
		return self._size

	@property
	def rect(self) -> pygame.Rect:
		return self._rect

	def reposition(self):
		self._update_container_properties()

		self._pos.update(
			self.ui_pos[0].get_pixels(self.container_size[0]),
			self.ui_pos[1].get_pixels(self.container_size[1])
		)
		self._size.update(
			self.ui_size[0].get_pixels(self.container_size[0]),
			self.ui_size[1].get_pixels(self.container_size[1])
		)

		self._rect.topleft = self.pos + self.container_offset
		self._rect.size = self.size

	def add_action(self, trigger: UIActionTriggers, action: Callable[..., None], action_args: tuple = ()) -> "UIElement":
		self._actions[trigger].append((action, action_args))
		return self

	def _perform_action(self, trigger: UIActionTriggers):
		for action in self._actions[trigger]:
			action[0](*action[1])

	def update(self, delta: float):
		self.time += delta

		if self._rect.collidepoint(pygame.mouse.get_pos()):
			if not self.hovered:
				self.hovered = True
				self._perform_action(UIActionTriggers.ON_HOVER_ENTER)

				self.time = 0

				if InputManager.mouse_pressed[0]:
					self.clicked = True
					self._perform_action(UIActionTriggers.ON_CLICK_DOWN)

			if InputManager.mouse_down[0]:
				self.clicked = True
				self._perform_action(UIActionTriggers.ON_CLICK_DOWN)

				self.time = 0
			if InputManager.mouse_up[0]:
				self.clicked = False
				self._perform_action(UIActionTriggers.ON_CLICK_UP)

				self.time = 0
		else:
			if self.hovered:
				self.hovered = False
				self._perform_action(UIActionTriggers.ON_HOVER_EXIT)

				self.time = 0

			if self.clicked:
				self.clicked = False

				self.time = 0

	def draw(self, screen: pygame.Surface):
		pass


UIElementType = TypeVar('UIElementType', bound=UIElement)
