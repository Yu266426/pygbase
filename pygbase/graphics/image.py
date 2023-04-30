import logging
import math

import pygame

from ..common import Common


class Image:
	def __init__(self, image: str | pygame.SurfaceType, scale: float | tuple[float, float], rotatable: bool, scale_by: bool = True):
		if isinstance(image, str):
			image: pygame.SurfaceType = pygame.image.load(image).convert_alpha()

		if scale_by:
			self.image = pygame.transform.scale_by(image.convert_alpha(), scale)
		else:
			self.image = pygame.transform.scale(image.convert_alpha(), scale)

		self.rotatable = rotatable

		self.rotate_angle = Common.get_value("rotate_resolution")
		self.angled_images = []

		if rotatable:
			self._generate_rotations()

	def _generate_rotations(self):
		self.angled_images.clear()

		num_rotations = math.ceil(360 / self.rotate_angle)
		current_angle: float = 0.0
		for angle in range(num_rotations):
			self.angled_images.append(pygame.transform.rotate(self.image, current_angle))
			current_angle += self.rotate_angle

	def scale(self, scale: tuple[float, float]) -> "Image":
		return Image(self.image, scale, self.rotatable, scale_by=False)

	def scale_by(self, scale: tuple[float, float]) -> "Image":
		return Image(self.image, scale, self.rotatable, scale_by=True)

	def get_image(self, angle: float = 0) -> pygame.Surface:
		if angle != 0:
			return self._get_angled_image(angle)
		else:
			return self.image

	def _get_angled_image(self, angle: float):
		if not self.rotatable:
			logging.error("Non-zero values of rotation not allowed for non-rotatable image")
			raise ValueError("Non-zero values of rotation not allowed for non-rotatable image")

		angle %= 360

		image_index = int(angle / self.rotate_angle)
		return self.angled_images[image_index]

	def draw(self, screen: pygame.Surface, rect: pygame.Rect | tuple[int | float, int | float], angle: float = 0, flip: bool = False, special_flags: int = 0):
		if angle != 0:
			image = self._get_angled_image(angle)
		else:
			image = self.image

		if flip:
			image = pygame.transform.flip(image, True, False)

		screen.blit(image, rect, special_flags=special_flags)
