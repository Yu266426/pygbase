import pygame

from .common import Common


class DebugDisplay:
	_active: bool = False

	_debug_surface: pygame.Surface

	_show_timing_debug: bool = False
	_timing_font: pygame.font.SysFont
	_timing_surf: pygame.Surface

	@classmethod
	def init(cls) -> None:
		cls._debug_surface = pygame.Surface(Common.get_value("screen_size"), flags=pygame.SRCALPHA)
		cls._timing_font: pygame.font.SysFont = pygame.font.SysFont("arial", 30)

	@classmethod
	def show(cls):
		cls._active = True

	@classmethod
	def hide(cls):
		cls._active = False

	@classmethod
	def toggle(cls):
		cls._active = not cls._active

	@classmethod
	def show_fps(cls):
		cls._show_timing_debug = True

	@classmethod
	def hide_fps(cls):
		cls._show_timing_debug = False

	@classmethod
	def toggle_fps(cls):
		cls._show_timing_debug = not cls._show_timing_debug

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
	def update_timing_text(cls, delta: float, fps: float, ):
		if cls._show_timing_debug:
			cls._timing_surf = cls._timing_font.render(f"fps: {fps}, delta: {delta}", True, "yellow")

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
	def draw(cls, surface: pygame.Surface) -> None:
		"""
		Called at end of frame on top of everything
		"""
		if cls._active:
			surface.blit(cls._debug_surface, (0, 0))

		if cls._show_timing_debug:
			rect = cls._timing_surf.get_rect(topright=(Common.get_value("screen_width") - 20, 20))
			surface.blit(cls._timing_surf, rect)
