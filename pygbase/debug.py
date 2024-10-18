import pygame

from .common import Common


class DebugDisplay:
	_active: bool = False

	_debug_surface: pygame.Surface

	@classmethod
	def init(cls) -> None:
		cls._debug_surface = pygame.Surface(Common.get_value("screen_size"), flags=pygame.SRCALPHA)

	@classmethod
	def show(cls) -> None:
		cls._active = True

	@classmethod
	def hide(cls) -> None:
		cls._active = False

	@classmethod
	def is_active(cls) -> bool:
		return cls._active

	@classmethod
	def clear(cls) -> None:
		"""
		Called at the beginning of a frame to clear the debug surface
		"""
		if cls._active:
			cls._debug_surface.fill((0, 0, 0, 0))

	@classmethod
	def draw_rect(cls, rect: pygame.typing.RectLike, color: pygame.typing.ColorLike, width: int = 1):
		if cls._active:
			pygame.draw.rect(cls._debug_surface, color, rect, width=width)

	@classmethod
	def draw_circle(cls, center: pygame.typing.Point, radius: float, color: pygame.typing.ColorLike, width: int = 1):
		if cls._active:
			pygame.draw.circle(cls._debug_surface, color, center, radius, width=width)

	@classmethod
	def draw_line(cls, start: pygame.typing.Point, end: pygame.typing.Point, color: pygame.typing.ColorLike, width: int = 1):
		if cls._active:
			pygame.draw.line(cls._debug_surface, color, start, end, width=width)

	@classmethod
	def draw(cls, screen: pygame.Surface) -> None:
		"""
		Called at end of frame on top of everything
		"""
		if cls._active:
			screen.blit(cls._debug_surface, (0, 0))
