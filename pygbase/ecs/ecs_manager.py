from collections import defaultdict

from .component import Component
from .entity import Entity
from .query import Query


class ECS:
	def __init__(self):
		self._next_entity_id = 0
		self._entity_components: dict[int, set[type[Component]]] = {}
		self._components: dict[type[Component], dict[int, Component]] = {}
		self._component_entities: dict[type[Component], set[int]] = defaultdict(set)

	def create_entity[T: Entity](
		self, base: type[T] = Entity, components: dict[type[Component], tuple[...]] | None = None
	) -> T:
		"""
		:param base: Base class of entity to spawn
		:param components: Components entity should spawn with (overrides default components)
		:return: Newly created entity
		"""

		new_entity = base(self._next_entity_id)
		self._next_entity_id += 1

		entity_components = {}
		entity_components.update(new_entity.default_components)
		if components is not None:
			entity_components.update(components)

		self._entity_components[new_entity.id] = set(entity_components.keys())

		# Create default components for the entity
		for component_type, component_data in entity_components.items():
			self._components.setdefault(component_type, {})[new_entity.id] = component_type(
				*component_data
			)
			self._component_entities[component_type].add(new_entity.id)

		return new_entity

	def remove_entity(self, entity: Entity):
		component_types = self._entity_components.pop(entity.id, None)
		if component_types is None:
			return

		for component_type in component_types:
			components = self._components.get(component_type)

			if components is not None and entity.id in components:
				del components[entity.id]

				if not components:
					del self._components[component_type]

			component_entities = self._component_entities.get(component_type)
			component_entities.discard(entity.id)
			if not component_entities:
				del self._component_entities[component_type]

	def set_component[T: Component](self, entity: Entity, component: T):
		component_type = type(component)
		self._entity_components[entity.id].add(component_type)
		self._component_entities[component_type].add(entity.id)
		self._components.setdefault(component_type, {})[entity.id] = component

	def get_component[T: Component](self, entity: Entity, component_type: type[T]) -> T | None:
		components = self._components.get(component_type)
		if components is not None:
			return components.get(entity.id)

		return None

	def remove_component[T: Component](self, entity: Entity, component_type: type[T]):
		component_types = self._entity_components.get(entity.id)
		if component_types is None or component_type not in component_types:
			return
		component_types.remove(component_type)

		components = self._components.get(component_type)
		if components is not None:
			del components[entity.id]

			if not components:
				del self._components[component_type]

		component_entities = self._component_entities.get(component_type)
		component_entities.discard(entity.id)
		if not component_entities:
			del self._component_entities[component_type]

	def query(self, query: Query) -> list[tuple[Entity, Component, ...]]:
		pass
