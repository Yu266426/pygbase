import pygame

from ..camera import Camera
from ..resources import ResourceManager


class Animation:
	def __init__(self, pos: tuple, sprite_sheet_name: str, anim_start_index: int, length: int, looping=True):
		self.pos = pygame.Vector2(pos)

		self.sprite_sheet_id = sprite_sheet_name
		self.anim_start_index = anim_start_index
		self.length = length

		self.looping = looping

		self.frame = 0.0
		self.images: list[pygame.Surface] = []

		self._load_animation()

	def _load_animation(self):
		for index in range(self.anim_start_index, self.anim_start_index + self.length + 1):
			self.images.append(ResourceManager.get_resource(2, self.sprite_sheet_id).get_image(index))

	def change_frame(self, amount: float):
		self.frame += amount

		if self.frame >= self.length:
			if self.looping:
				self.frame = 0
			else:
				self.frame = self.length - 0.01
		if self.frame < 0:
			if self.looping:
				self.frame = self.length - 0.01
			else:
				self.frame = 0

	def draw(self, display: pygame.Surface, camera: Camera, flag=0):
		display.blit(self.images[int(self.frame)], self.pos - camera.target, special_flags=flag)
