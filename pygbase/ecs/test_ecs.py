import pygame

from .component import Component
from .ecs_manager import ECS
from .entity import Entity


class CustomComponent(Component):
	def __init__(self, int_data: int, str_data: str):
		self.int_data = int_data
		self.str_data = str_data


class CustomComponent2(Component):
	def __init__(self, pos: pygame.typing.Point):
		self.pos = pygame.Vector2(pos)


class CustomEntity(Entity):
	default_components = {CustomComponent: (1, "test")}


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
	ecs = ECS()
	entity = ecs.create_entity(CustomEntity)

	assert entity.id == 0
	assert ecs._entities[entity.id] == {CustomComponent}

	custom_component = ecs.get_component(entity, CustomComponent)
	assert custom_component.int_data == 1
	assert custom_component.str_data == "test"

	custom_component.int_data = 10
	assert ecs.get_component(entity, CustomComponent).int_data == 10


def test_make_entity_with_component_overrides():
	ecs = ECS()
	entity = ecs.create_entity(CustomEntity)

	assert ecs.get_component(entity, CustomComponent).int_data == 1
	assert ecs.get_component(entity, CustomComponent).str_data == "test"

	entity_with_override = ecs.create_entity(
		CustomEntity, {CustomComponent: (10, "test2"), CustomComponent2: ((50, 50),)}
	)
	assert ecs.get_component(entity_with_override, CustomComponent).int_data == 10
	assert ecs.get_component(entity_with_override, CustomComponent).str_data == "test2"

	assert ecs.get_component(entity_with_override, CustomComponent2).pos == pygame.Vector2(50, 50)

	entity_with_custom2 = ecs.create_entity(CustomEntity, {CustomComponent2: ((10, 10),)})
	assert ecs.get_component(entity_with_custom2, CustomComponent).int_data == 1
	assert ecs.get_component(entity_with_custom2, CustomComponent).str_data == "test"

	assert ecs.get_component(entity_with_custom2, CustomComponent2).pos == pygame.Vector2(10, 10)
