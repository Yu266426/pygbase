import pygame

from ..camera import Camera
from ..common import Common


class Shadow:
	cached_shadows: list[pygame.Surface] = []

	def __init__(self, pos: pygame.typing.Point, size: float):
		self.pos = pygame.Vector2(pos)
		self.size = size

		self.radius_interval = Common.get("lighting_radius_interval")

		self.surf = self.cached_shadows[int(size / self.radius_interval)].copy()
		self.surf_rect = self.surf.get_rect(center=self.pos)

	def init_surf(self, brightness: int):
		self.surf.fill((brightness, brightness, brightness), special_flags=pygame.BLEND_MULT)

	def link_pos(self, pos: pygame.Vector2) -> "Shadow":
		self.pos = pos
		return self

	def draw(self, surface: pygame.Surface, camera: Camera):
		self.surf_rect.center = self.pos
		surface.blit(self.surf, camera.world_to_screen_rect(self.surf_rect))
