import pygame


class Camera:
	def __init__(self, pos: tuple[int | float, int | float] | pygame.Vector2 = (0, 0)):
		self.target: pygame.Vector2 = pygame.Vector2(pos)

	def set_target(self, target: pygame.Vector2):
		self.target: pygame.Vector2 = target.copy()

	def lerp_to_target(self, target: pygame.Vector2, amount: float):
		amount = max(0.0, min(amount, 1.0))
		if self.target.distance_to(target) < 1:
			self.target = target
		else:
			self.target = self.target.lerp(target, amount)

	def screen_to_world(self, pos: pygame.Vector2 | tuple):
		return pygame.Vector2(pos[0] + self.target.x, pos[1] + self.target.y)

	def world_to_screen(self, pos: pygame.Vector2 | tuple):
		return pos[0] - self.target.x, pos[1] - self.target.y
