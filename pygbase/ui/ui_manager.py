import pygame

from .ui_element import UIElementType
from .ui_elements import Frame
from .values import UIValue


class UIManager:
	def __init__(self):
		self._frames: list[Frame] = [Frame((UIValue(0, False), UIValue(0, False)), (UIValue(1, False), UIValue(1, False)))]

	@property
	def base_container(self):
		return self._frames[0]

	def add_frame(self, frame: Frame) -> Frame:
		self._frames.append(frame)
		return frame

	def add_element(self, element: UIElementType, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> UIElementType:
		return self._frames[0].add_element(element, align_with_previous=align_with_previous, add_on_to_previous=add_on_to_previous)

	def remove_element(self, element: UIElementType):
		self._frames[0].remove_element(element)

	def on_ui(self) -> bool:
		for frame in self._frames[1:]:
			if frame.active:
				if frame.rect.collidepoint(*pygame.mouse.get_pos()):
					return True

		for element in self._frames[0].elements:
			if element.rect.collidepoint(*pygame.mouse.get_pos()):
				return True

		return False

	def update(self, delta: float):
		for frame in self._frames:
			frame.update(delta)

	def draw(self, surface: pygame.Surface):
		for frame in self._frames:
			frame.draw(surface)
