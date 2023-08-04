import logging
import math

import pygame

from ..common import Common


class Image:
	def __init__(self, image: str | pygame.Surface, scale: float | tuple[float, float], rotatable: bool, scale_by: bool = True):
		if isinstance(image, str):
			image: pygame.Surface = pygame.image.load(image).convert_alpha()

		if scale_by:
			self.image = pygame.transform.scale_by(image, scale).convert_alpha()
		else:
			self.image = pygame.transform.scale(image, scale).convert_alpha()

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
			self.angled_images.append(pygame.transform.rotate(self.image, current_angle).convert_alpha())
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

	def draw(self, surface: pygame.Surface, pos: pygame.Vector2 | tuple[float, float], angle: float = 0, flip: tuple[bool, bool] = (False, False), draw_pos: str = "topleft", flags: int = 0):
		factor = -1 if flip[0] ^ flip[1] else 1  # Exclusive or
		image = self.get_image(angle * factor)

		if flip:
			image = pygame.transform.flip(image, *flip)

		origin = self.get_image()
		if draw_pos == "topleft":
			center = origin.get_rect(topleft=pos).center
		elif draw_pos == "center":
			center = origin.get_rect(center=pos).center
		elif draw_pos == "midbottom":
			center = origin.get_rect(midbottom=pos).center
		elif draw_pos == "none":
			center = image.get_rect(topleft=pos).center
		else:
			raise ValueError(f"{draw_pos} not a valid position.")

		rect = image.get_rect(center=center)
		surface.blit(image, rect, special_flags=flags)
