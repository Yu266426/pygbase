from .camera import Camera
from .common import Common
from .events import EventManager
from .game_state import GameState
from .inputs import InputManager
from .resources import ResourceType, ResourceManager


def init(screen_size: tuple[int, int]):
	Common.add_value("screen_width", screen_size[0])
	Common.add_value("screen_height", screen_size[1])

	EventManager.init()
	InputManager.register_handlers()


def add_resource_type(type_id: int, resource_type: ResourceType):
	ResourceManager.add_resource_type(type_id, resource_type)
