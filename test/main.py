import logging
import pathlib

import pygame
from menu import Menu

import pygbase

if __name__ == "__main__":
	CURRENT_DIR = pathlib.Path.cwd() / "test"

	pygbase.init((800, 800))
	pygbase.Debug.show()
	pygbase.Debug.show_fps()

	pygbase.add_image_resource("image", 1, str(CURRENT_DIR / "images"))

	pygbase.Events.add_handler(
		"all",
		pygame.KEYDOWN,
		handler=lambda e: pygbase.Events.post_event(pygame.QUIT)
		if e.key == pygame.K_ESCAPE
		else None,
	)

	pygbase.Events.create_custom_event("test")

	pygbase.Events.add_handler("all", "test", lambda e: logging.info("Received Test Event"))

	pygbase.Events.post_event("test")

	app = pygbase.App(Menu)
	app.run()

	pygbase.quit()
