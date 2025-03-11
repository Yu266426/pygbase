import pygame

import pygbase

from pygbase.ui import *


class ParticlePlayground(pygbase.GameState, name="particles"):
	def __init__(self):
		super().__init__()

		from menu import Menu
		with Button(self.set_next_state_type, callback_args=(Menu, ()), pos=(10, 10), size=(150, Fit())) as ui:
			with Image("button", size=(Grow(), Fit()), x_align=XAlign.CENTER, y_align=YAlign.CENTER):
				Text("Back", 20, "white")

		ui.resolve_layout(pygbase.Common.get("screen_size"))
		self.ui = ui

		self.camera_controller = pygbase.CameraController()
		self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

		self.particle_manager = pygbase.ParticleManager(chunk_size=100)
		self.circle_spawner = self.particle_manager.add_spawner(
			pygbase.CircleSpawner(
				(400, 400),
				0.05, 200,
				400,
				True, "test",
				self.particle_manager
			)
		)

		self.mouse_spawner = self.particle_manager.add_spawner(
			pygbase.CircleSpawner(
				self.mouse_pos, 0.01, 30, 50, False, "test",
				self.particle_manager
			).link_pos(self.mouse_pos)
		)

		self.attractor_strength = 40000
		self.mouse_attractor = self.particle_manager.add_affector(
			pygbase.AffectorTypes.ATTRACTOR,
			pygbase.ParticleAttractor(self.mouse_pos, 200, self.attractor_strength).link_pos(self.mouse_pos)
		)

	def update(self, delta: float):
		self.ui.update(delta)
		self.camera_controller.update(delta)
		self.mouse_pos.update(self.camera_controller.camera.screen_to_world(pygame.mouse.get_pos()))

		if pygbase.Input.mouse_pressed(0):
			self.mouse_spawner.active = True
		else:
			self.mouse_spawner.active = False

		if pygbase.Input.mouse_pressed(2):
			self.mouse_attractor.strength = self.attractor_strength
		else:
			self.mouse_attractor.strength = 0

		self.particle_manager.update(delta)

	def draw(self, surface: pygame.Surface):
		surface.fill((20, 20, 20))

		self.particle_manager.draw(surface, self.camera_controller.camera)

		self.ui.draw(surface)
