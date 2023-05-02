import logging

import pygame

from .ui_elements import UIElement, Frame


class UIManager:
	def __init__(self):
		self._frames: list[Frame] = [Frame((0, 0), (1, 1))]

	@property
	def base_container(self):
		return self._frames[0]

	def add_frame(self, frame: Frame) -> Frame:
		self._frames.append(frame)
		return frame

	def add_element(self, element: UIElement, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> Frame:
		return self._frames[0].add_element(element, align_with_previous=align_with_previous, add_on_to_previous=add_on_to_previous)

	def on_ui(self) -> bool:
		for frame in self._frames:
			if frame.active:
				if frame._rect.collidepoint(*pygame.mouse.get_pos()):
					return True

		return False

	def update(self, delta: float):
		for frame in self._frames:
			frame.update(delta)

	def draw(self, screen: pygame.Surface):
		for frame in self._frames:
			frame.draw(screen)
