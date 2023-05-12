import logging

import pygame

import pygbase.utils
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
from .transition_states import FadeTransition
from .ui.enums import UIActionTriggers
from .ui.ui_elements import Frame, ImageElement, TextElement, TextSelectionMenu, Button
from .ui.ui_manager import UIManager


def init(screen_size: tuple[int, int], logging_level=logging.DEBUG, rotate_resolution: float = 0.5):
	logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

	pygame.init()

	Common.set_value("screen_width", screen_size[0])
	Common.set_value("screen_height", screen_size[1])

	Common.set_value("rotate_resolution", rotate_resolution)

	EventManager.init()
	InputManager.register_handlers()


def add_resource_type(type_id: int, resource_type: ResourceType):
	Common.add_resource_type(resource_type.name, type_id)

	ResourceManager.add_resource_type(type_id, resource_type)


def add_image_resource(name: str, type_id: int, dir_path: str):
	def load_image(data: dict, resource_path: str):
		scale = data["scale"]
		rotatable = data["rotatable"]

		return Image(resource_path, scale, rotatable)

	add_resource_type(type_id, ResourceType(
		name, dir_path, ".png",
		{"scale": 1, "rotatable": False},
		None,
		load_image
	))


def add_sprite_sheet_resource(name: str, type_id: int, dir_path: str, default_scale: float = 1):
	add_resource_type(type_id, ResourceType(
		name, dir_path, ".png",
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


def add_sound_resource(name: str, type_id: int, dir_path: str, sound_ending: str):
	def load_sound(data: dict, resource_path: str):
		volume = data["volume"]

		sound = pygame.mixer.Sound(resource_path)
		sound.set_volume(volume)
		return sound

	add_resource_type(type_id, ResourceType(
		name, dir_path, sound_ending,
		{
			"volume": 1
		},
		None,
		load_sound
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
	Common.add_particle_setting(name, colour, size, size_decay, velocity_decay, gravity, effector)


def quit():
	pygame.quit()
