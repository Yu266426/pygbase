import pygame

from .image import Image
from ..camera import Camera
from ..ui.text import Text


class SpriteSheet:
	def __init__(self, data: dict, resource_path: str, default_scale: float):
		# Data info
		self.n_rows: int = data["rows"]
		self.n_cols: int = data["columns"]
		self.scale: int = data["scale"] if data["scale"] != 0 else default_scale
		self.rotatable: bool = data["rotatable"]
		self.tile_width: int = data["tile_width"] * self.scale
		self.tile_height: int = data["tile_height"] * self.scale

		# Load Sprite Sheet
		self.image: pygame.Surface = pygame.image.load(resource_path).convert_alpha()
		self.image.set_colorkey((0, 0, 0))
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))

		# Automatically set n_rows and n_cols if needed
		if self.n_rows == 0:
			self.n_rows = int(self.image.get_height() / self.tile_height)
		if self.n_cols == 0:
			self.n_cols = int(self.image.get_width() / self.tile_width)

		self._images: list[Image] = []

		self._load_sprite_sheet()

		self.length = len(self._images)

	def _load_image(self, row, col):
		rect = pygame.Rect(col * self.tile_width, row * self.tile_height, self.tile_width, self.tile_height)
		# image = self.image.subsurface(rect)  # Unusable due to transparency issue
		# image = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
		# image.blit(self.image, (0, 0), rect)
		# print(image)
		image = self.image.subsurface(rect)

		self._images.append(Image(image, 1, self.rotatable))

	def _load_sprite_sheet(self):
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				self._load_image(row, col)

	def get_image(self, index: int) -> Image:
		return self._images[index]

	def draw_sheet(self, display: pygame.Surface, camera: Camera):
		display.blit(self.image, -camera.pos)

		# TODO: Fix
		text = Text((0, 0), "arial", 100, "white", use_sys=True)
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				text.pos = (col * self.tile_width - camera.pos.x, row * self.tile_height - camera.pos.y)
				text.reposition()
				text.draw(display)
