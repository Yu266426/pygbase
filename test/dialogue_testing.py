import pygame

import pygbase


class DialogueTesting(pygbase.GameState, name="dialogue"):
	def __init__(self):
		super().__init__()

		self.dialogue_manager = pygbase.DialogueManager(10, 0.02)
		from menu import Menu
		self.dialogue_manager.add_node(
			pygbase.DialogueNode("first", "This is a test message, I don't know if this will work")
		).add_option(
			"first", pygbase.DialogueOption("Next", next_node="second")
		).add_node(
			pygbase.DialogueNode("second", "The first one must have worked, what about this?")
		).add_option(
			"second", pygbase.DialogueOption("Back", callback=self.set_next_state_type, callback_args=(Menu, ()))
		)

	def update(self, delta: float):
		self.dialogue_manager.update(delta)

		if pygbase.Input.key_just_pressed(pygame.K_SPACE):
			self.dialogue_manager.set_current_node("first")

	def draw(self, surface: pygame.Surface):
		if self.dialogue_manager.current_node != "" and self.dialogue_manager.nodes[self.dialogue_manager.current_node].finished_displaying:
			surface.fill((40, 40, 40))
		else:
			surface.fill((20, 20, 20))

		self.dialogue_manager.draw(surface)
