import pygame

from .app import App
from .camera import Camera
from .common import Common
from .events import EventManager
from .game_state import GameState
from .graphics.animation import Animation, AnimationManager
from .graphics.sprite_sheet import SpriteSheet
from .inputs import InputManager
from .resources import ResourceType, ResourceManager


def init(screen_size: tuple[int, int]):
	pygame.init()

	Common.set_value("screen_width", screen_size[0])
	Common.set_value("screen_height", screen_size[1])

	EventManager.init()
	InputManager.register_handlers()


def add_resource_type(type_id: int, resource_type: ResourceType):
	Common.set_value(f"{resource_type.name}_res", type_id)

	ResourceManager.add_resource_type(type_id, resource_type)


def add_image_resource(name: str, type_id: int, dir_path: str):
	def load_image(data: dict, resource_path: str):
		scale = data["scale"]

		image = pygame.image.load(resource_path).convert_alpha()
		image = pygame.transform.scale_by(image, scale)
		return image

	add_resource_type(type_id, ResourceType(
		name, dir_path,
		{"scale": 1},
		None,
		load_image
	))


def add_sprite_sheet_resource(name: str, type_id: int, tile_scale: float, dir_path: str):
	add_resource_type(type_id, ResourceType(
		name, dir_path,
		{
			"rows": 0,
			"columns": 0,
			"tile_width": 0,
			"tile_height": 0,
			"scale": -1
		},
		lambda data: data["scale"] != -1,
		lambda data, resource_path: SpriteSheet(data, resource_path, tile_scale)
	))


def quit():
	pygame.quit()
