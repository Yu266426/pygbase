import logging

import pygame.typing

__all__ = [
	"App",
	"Camera",
	"CameraController",
	"GameState",
	"Timer",
	"FadeTransition",
	"LinearTween",
	"CubicTween",
]

import pygbase.utils

from .app import App
from .camera import Camera, CameraController
from .common import Common
from .debug import Debug
from .events import Events
from .game_state import GameState
from .graphics import *
from .graphics.image import Image
from .graphics.sprite_sheet import SpriteSheet
from .inputs import *
from .lighting import *
from .particles import *
from .resources import Resources, ResourceType
from .timer import Timer
from .transition_states import FadeTransition
from .tweens import CubicTween, LinearTween
from .ui import *


def init(
	screen_size: tuple[int, int],
	logging_level=logging.DEBUG,
	rotate_resolution: float = 0.5,
	max_light_radius: int = 600,
	max_shadow_radius: int = 50,
	light_radius_interval: int = 2,
	shadow_ratio: float = 1,
):
	logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

	pygame.init()

	Common.set_value("screen_width", screen_size[0])
	Common.set_value("screen_height", screen_size[1])
	Common.set_value("screen_size", screen_size)

	Common.set_value("rotate_resolution", rotate_resolution)

	Events.init()
	Input.register_handlers()

	lighting.init_lighting_system(
		max_light_radius, max_shadow_radius, light_radius_interval, shadow_ratio
	)

	Debug.init()


def add_resource_type(type_id: int, resource_type: ResourceType):
	Common.add_resource_type(resource_type.name, type_id)

	Resources.add_resource_type(type_id, resource_type)


def add_image_resource(name: str, type_id: int, dir_path: str, default_scale: float = 1):
	def load_image(data: dict, resource_path: str):
		scale = data["scale"]
		scale = scale if scale != 0 else default_scale
		rotatable = data["rotatable"]

		return Image(resource_path, scale, rotatable)

	add_resource_type(
		type_id,
		ResourceType(name, dir_path, ".png", {"scale": 0, "rotatable": False}, None, load_image),
	)


def add_sprite_sheet_resource(name: str, type_id: int, dir_path: str, default_scale: float = 1):
	add_resource_type(
		type_id,
		ResourceType(
			name,
			dir_path,
			".png",
			{
				"rows": 0,
				"columns": 0,
				"tile_width": 0,
				"tile_height": 0,
				"scale": -1,
				"rotatable": False,
			},
			lambda data: data["scale"] != -1,
			lambda data, resource_path: SpriteSheet(data, resource_path, default_scale),
		),
	)


def add_sound_resource(name: str, type_id: int, dir_path: str, sound_ending: str):
	def load_sound(data: dict, resource_path: str):
		volume = data["volume"]

		sound = pygame.mixer.Sound(resource_path)
		sound.set_volume(volume)
		return sound

	add_resource_type(
		type_id, ResourceType(name, dir_path, sound_ending, {"volume": 1}, None, load_sound)
	)


def add_particle_setting(
	name: str,
	colour: list[pygame.typing.ColorLike],
	size: tuple[float, float],
	size_decay: tuple[float, float],
	velocity_decay: tuple[float, float],
	gravity: tuple[float, float],
	effector: bool,
	bounce: tuple[tuple[float, float], tuple[float, float]],
):
	Common.add_particle_setting(
		name, colour, size, size_decay, velocity_decay, gravity, effector, bounce
	)


def quit():  # NoQA
	pygame.quit()
