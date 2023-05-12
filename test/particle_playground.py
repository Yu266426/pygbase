import pygame

import pygbase


class ParticlePlayground(pygbase.GameState, name="particles"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIManager()

		from game import Game
		self.ui.add_element(
			pygbase.Button(
				(0.02, 0.02), (0.2, 0),
				pygbase.Common.get_resource_type("image"), "button",
				self.ui.base_container,
				self.set_next_state_type, callback_args=(Game, ()),
				text="Back",
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

		self.particles.draw(screen, self.camera)

		self.ui.draw(screen)
