from .events import EventManager
from .inputs import InputManager
from .resources import ResourceType, ResourceManager

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 800


def init():
	EventManager.init()
	InputManager.register_handlers()


def add_resource_type(type_id: int, resource_type: ResourceType):
	ResourceManager.add_resource_type(type_id, resource_type)
