import pygame.freetype


class Text:
	def __init__(self, pos: tuple | pygame.Vector2, font_name: str, size: int | float, colour: pygame.Color | str | tuple, text: str = "", use_sys: bool = False):
		if use_sys:
			self.font = pygame.freetype.SysFont(font_name, size)
		else:
			self.font = pygame.freetype.Font(font_name, size)

		self.text = text

		self.colour = colour

		self.pos = pos

		self.rendered_text: tuple[pygame.Surface, pygame.Rect] | None = None
		self.render_text()

	def set_text(self, text: str):
		self.text = text
		self.render_text()

	def render_text(self):
		self.rendered_text = self.font.render(self.text, self.colour)
		self.rendered_text = self.rendered_text[0].convert_alpha(), self.rendered_text[1]

	def draw(self, screen: pygame.Surface, draw_from: str = "l", pos=None) -> None:
		if pos is None:
			if draw_from == "l":
				screen.blit(self.rendered_text[0], self.pos)
			elif draw_from == "c":
				screen.blit(self.rendered_text[0], (self.pos[0] - self.rendered_text[1].width / 2, self.pos[1]))
			elif draw_from == "r":
				screen.blit(self.rendered_text[0], (self.pos[0] - self.rendered_text[1].width, self.pos[1]))
			else:
				raise ValueError(f"{draw_from} is not a valid position")
		else:
			if draw_from == "l":
				screen.blit(self.rendered_text[0], pos)
			elif draw_from == "c":
				screen.blit(self.rendered_text[0], (-self.rendered_text[1].width / 2 + pos[0], pos[1]))
			elif draw_from == "r":
				screen.blit(self.rendered_text[0], (-self.rendered_text[1].width + pos[0], pos[1]))
			else:
				raise ValueError(f"{draw_from} is not a valid position")
