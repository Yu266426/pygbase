import logging
import pathlib

import pygame

import pygbase
from menu import Menu


def toggle_debug(event: pygame.Event):
	if event.key == pygame.K_F3:
		pygbase.Debug.toggle()
	if event.key == pygame.K_F4:
		pygbase.Debug.toggle_fps()


if __name__ == "__main__":
	CURRENT_DIR = pathlib.Path.cwd() / "test"

	pygbase.init((800, 800))
	# pygbase.Debug.show()
	pygbase.Debug.show_fps()
	#
	pygbase.add_image_resource("image", 1, str(CURRENT_DIR / "images"))

	pygbase.add_particle_setting(
		"test",
		[(143, 186, 255), (102, 237, 255), (82, 154, 255), (255, 40, 30), (255, 90, 0), (255, 154, 0)],
		(4, 7),
		(3, 5),
		(0.6, 1.2),
		(0, 0),
		True,
		((0, 0), (0, 0))
	)

	pygbase.Events.add_handler(
		"all",
		pygame.KEYDOWN,
		handler=lambda e: pygbase.Events.post_event(pygame.QUIT)
		if e.key == pygame.K_ESCAPE
		else None,
	)

	# Debug toggle
	pygbase.Events.add_handler(
		"all",
		pygame.KEYDOWN,
		handler=toggle_debug
	)

	pygbase.Events.create_custom_event("test")

	pygbase.Events.add_handler("all", "test", lambda e: logging.info("Received Test Event"))

	pygbase.Events.post_event("test")

	app = pygbase.App(Menu)
	app.run()

	pygbase.quit()
