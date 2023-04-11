import logging

import pygame

from .app import App
from .camera import Camera
from .common import Common
from .events import EventManager
from .game_state import GameState
from .graphics.animation import Animation, AnimationManager
from .graphics.image import Image
from .graphics.sprite_sheet import SpriteSheet
from .inputs import InputManager
from .particles.particle_affectors import ParticleAttractor
from .particles.particle_manager import ParticleManager
from .particles.particle_settings import ParticleOptions
from .particles.particle_spawners import ParticleSpawner, PointSpawner, CircleSpawner, RectSpawner
from .resources import ResourceType, ResourceManager
from .timer import Timer


def init(screen_size: tuple[int, int], logging_level=logging.DEBUG, rotate_resolution: float = 0.5):
	logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

	pygame.init()

	Common.set_value("screen_width", screen_size[0])
	Common.set_value("screen_height", screen_size[1])

	Common.set_value("rotate_resolution", rotate_resolution)

	Common.set_value("particle_settings", {
		"default": {
			ParticleOptions.COLOUR: ["white"],
			ParticleOptions.SIZE: (4.0, 7.0),
			ParticleOptions.SIZE_DECAY: (3.0, 5.0),
			ParticleOptions.VELOCITY_DECAY: (1.8, 2.2),
			ParticleOptions.GRAVITY: (0, 0),
			ParticleOptions.EFFECTOR: True
		}
	})

	EventManager.init()
	InputManager.register_handlers()


def add_resource_type(type_id: int, resource_type: ResourceType):
	Common.set_value(f"{resource_type.name}_res", type_id)

	ResourceManager.add_resource_type(type_id, resource_type)


def add_image_resource(name: str, type_id: int, dir_path: str):
	def load_image(data: dict, resource_path: str):
		scale = data["scale"]
		rotatable = data["rotatable"]

		return Image(resource_path, scale, rotatable)

	add_resource_type(type_id, ResourceType(
		name, dir_path,
		{"scale": 1, "rotatable": False},
		None,
		load_image
	))


def add_sprite_sheet_resource(name: str, type_id: int, dir_path: str, default_scale: float = 1):
	add_resource_type(type_id, ResourceType(
		name, dir_path,
		{
			"rows": 0,
			"columns": 0,
			"tile_width": 0,
			"tile_height": 0,
			"scale": -1,
			"rotatable": False
		},
		lambda data: data["scale"] != -1,
		lambda data, resource_path: SpriteSheet(data, resource_path, default_scale)
	))


def add_particle_setting(
		name: str,
		colour: list,
		size: tuple[float, float],
		size_decay: tuple[float, float],
		velocity_decay: tuple[float, float],
		gravity: tuple[float, float],
		effector: bool
):
	particle_settings = Common.get_value("particle_settings")

	particle_settings[name] = {
		ParticleOptions.COLOUR: colour,
		ParticleOptions.SIZE: size,
		ParticleOptions.SIZE_DECAY: size_decay,
		ParticleOptions.VELOCITY_DECAY: velocity_decay,
		ParticleOptions.GRAVITY: gravity,
		ParticleOptions.EFFECTOR: effector
	}


def quit():
	pygame.quit()
