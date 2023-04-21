import pygame


class Camera:
	def __init__(self, pos: tuple[int | float, int | float] | pygame.Vector2 = (0, 0)):
		self.pos: pygame.Vector2 = pygame.Vector2(pos)

	def set_pos(self, target: pygame.Vector2):
		# set pos to target copy, so that if target's position changes our position does not change with it
		self.pos: pygame.Vector2 = target.copy()

	def lerp_to_target(self, target: pygame.Vector2, amount: float):
		# clamp amount so that it does not go above 1.0
		amount = max(0.0, min(amount, 1.0))
		if self.pos.distance_to(target) < 1:
			# correct any minor position error
			self.pos = target
		else:
			self.pos = self.pos.lerp(target, amount)

	# --- conversions
	def screen_to_world(self, pos: pygame.Vector2 | tuple):
		return pygame.Vector2(pos[0] + self.pos.x, pos[1] + self.pos.y)

	def world_to_screen(self, pos: pygame.Vector2 | tuple):
		return pos[0] - self.pos.x, pos[1] - self.pos.y
