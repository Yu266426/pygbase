import logging
import pathlib

import pygame

import pygbase
from menu import Menu

if __name__ == '__main__':
	CURRENT_DIR = pathlib.Path.cwd()

	pygbase.init((800, 800))
	pygbase.DebugDisplay.show()
	pygbase.DebugDisplay.show_fps()

	pygbase.add_image_resource("image", 1, str(CURRENT_DIR / "images"))

	pygbase.EventManager.add_handler(
		"all",
		pygame.KEYDOWN,
		handler=lambda e: pygbase.EventManager.post_event(pygame.QUIT) if e.key == pygame.K_ESCAPE else None
	)

	pygbase.EventManager.create_custom_event("test")

	pygbase.EventManager.add_handler(
		"all",
		"test",
		lambda e: logging.info("Received Test Event")
	)

	pygbase.EventManager.post_event("test")

	app = pygbase.App(Menu)
	app.run()

	pygbase.quit()
