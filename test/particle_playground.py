import pygame

import pygbase


class ParticlePlayground(pygbase.GameState, name="particles"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIScreen()
		self.button_frame = self.ui.add_frame(pygbase.Frame((20, 20), (100, 50), bg_colour=(50, 50, 50, 100)))

		from game import Game
		self.button_frame.add_element(
			pygbase.Button(
				(0, 0), pygbase.Common.get_resource_type("image"), "button",
				self.set_next_state_type, (Game, ()),
				size=(100, 50),
				text="Back"
			)
		)

		self.camera = pygbase.Camera()

		self.particles = pygbase.ParticleManager()
		self.circle_spawner = self.particles.add_spawner(
			pygbase.CircleSpawner(
				(400, 400),
				0.05, 100,
				200,
				True, "default",
				self.particles
			)
		)

	def update(self, delta: float):
		self.ui.update(delta)

		self.particles.update(delta)

	def draw(self, screen: pygame.Surface):
		screen.fill((20, 20, 20))
		self.ui.draw(screen)

		self.particles.draw(screen, self.camera)
