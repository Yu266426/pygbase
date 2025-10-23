from .component import Component
from .ecs_manager import ECS
from .entity import Entity


def test_make_entity():
	ecs = ECS()
	entity_1 = ecs.create_entity()
	entity_2 = ecs.create_entity()
	entity_3 = ecs.create_entity()
	entity_4 = ecs.create_entity()

	assert entity_1.id == 0
	assert entity_2.id == 1
	assert entity_3.id == 2
	assert entity_4.id == 3


def test_make_custom_entity():
	class CustomComponent(Component):
		def __init__(self, int_data: int, str_data: str):
			self.int_data = int_data
			self.str_data = str_data

	class CustomEntity(Entity):
		default_components = {CustomComponent: (1, "test")}

	ecs = ECS()
	entity = ecs.create_entity(CustomEntity)

	assert entity.id == 0
	assert ecs._entities[entity.id] == {CustomComponent}

	custom_component = ecs.get_component(entity, CustomComponent)
	assert custom_component.int_data == 1
	assert custom_component.str_data == "test"

	custom_component.int_data = 10
	assert ecs.get_component(entity, CustomComponent).int_data == 10
