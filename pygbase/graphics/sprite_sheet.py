import pygame

from ..camera import Camera
from data.modules.base.constants import TILE_SCALE
from ..ui.text import Text


class SpriteSheet:
	def __init__(self, data: dict, resource_path: str):
		# Data info
		self.n_rows: int = data["rows"]
		self.n_cols: int = data["columns"]
		self.scale: int = data["scale"] if data["scale"] != 0 else TILE_SCALE
		self.tile_width: int = data["tile_width"] * self.scale
		self.tile_height: int = data["tile_height"] * self.scale

		# Sprite Sheet
		self.image: pygame.surface = pygame.image.load(resource_path).convert_alpha()
		self.image.set_colorkey((0, 0, 0))
		self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))

		self._images: list = []

		self._load_sprite_sheet()

		self.length = len(self._images)

	def _load_image(self, row, col):
		rect = pygame.Rect(col * self.tile_width, row * self.tile_height, self.tile_width, self.tile_height)
		image = pygame.Surface(size=rect.size, flags=pygame.SRCALPHA).convert_alpha()
		image.blit(self.image, (0, 0), rect)

		self._images.append(image)

	def _load_sprite_sheet(self):
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				self._load_image(row, col)

	def get_image(self, index: int) -> pygame.Surface:
		return self._images[index]

	def draw_sheet(self, display: pygame.Surface, camera: Camera):
		display.blit(self.image, -camera.target)

		# TODO: Fix
		text = Text((0, 0), "arial", 100, "white", use_sys=True)
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				text.draw(display, pos=(col * self.tile_width - camera.target.x, row * self.tile_height - camera.target.y))
