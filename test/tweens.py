import pygame

import pygbase


class Tweens(pygbase.GameState, name="tweens"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIManager()

		from menu import Menu
		self.back_button = self.ui.add_element(
			pygbase.Button(
				(pygbase.UIValue(0.02, False), pygbase.UIValue(0.02, False)),
				(pygbase.UIValue(0.2, False), pygbase.UIValue(0)),
				"image", "button", self.ui.base_container,
				self.set_next_state_type, (Menu, ()), "Back"
			)
		)

		self.tween_time = 3
		self.tween_values = (0, 0.2, 0.7, 1)

		self.tweens = [
			pygbase.LinearTween(self.tween_values, self.tween_time),
			pygbase.CubicTween(self.tween_values, self.tween_time)
		]

	def update(self, delta: float):
		self.ui.update(delta)

		for tween in self.tweens:
			tween.tick(delta)

			if tween.value() == self.tween_values[-1]:
				tween.set_progress(0)

	def draw(self, surface: pygame.Surface):
		surface.fill((20, 20, 20))

		for tween_value in self.tween_values:
			pygame.draw.line(surface, (50, 50, 50), (40 + (800 - 120) * tween_value, 100), (40 + (800 - 120) * tween_value, 700))

		for index, tween in enumerate(self.tweens):
			pygame.draw.line(surface, "light blue", (40, 150 + 50 * index), (800 - 80, 150 + 50 * index))
			pygame.draw.circle(surface, "yellow", (40 + (800 - 120) * tween.value(), 150 + 50 * index), 5)

		self.ui.draw(surface)
