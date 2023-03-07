import pathlib

import pygbase
from game import Game

if __name__ == '__main__':
	CURRENT_DIR = pathlib.Path.cwd()

	pygbase.init((800, 800))

	pygbase.add_image_resource("image", 1, str(CURRENT_DIR / "images"))

	app = pygbase.App(Game)
	app.run()

	pygbase.quit()
