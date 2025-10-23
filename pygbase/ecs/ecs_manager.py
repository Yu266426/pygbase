from .component import Component
from .entity import Entity
from .query import Query


class ECS:
	def __init__(self):
		self._next_entity_id = 0
		self._entities: dict[int, set[type[Component]]] = {}
		self._components: dict[type[Component], dict[int, Component]] = {}

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

		self._entities[new_entity.id] = set(entity_components.keys())

		# Create default components for the entity
		for component_type, component_data in entity_components.items():
			self._components.setdefault(component_type, {})[new_entity.id] = component_type(
				*component_data
			)

		return new_entity

	def remove_entity(self, entity: Entity):
		pass

	def set_component[T: Component](self, entity: Entity, component: T):
		component_type = type(component)
		self._entities[entity.id].add(component_type)
		self._components.setdefault(component_type, {})[entity.id] = component

	def get_component[T: Component](self, entity: Entity, component_type: type[T]) -> T | None:
		components = self._components.get(component_type)
		if components is not None:
			return components.get(entity.id)

		return None

	def remove_component[T: Component](self, entity: Entity, component_type: type[T]):
		self._entities[entity.id].remove(component_type)

		components = self._components.get(component_type)
		if components is not None:
			del components[entity.id]

	def query(self, query: Query) -> list[tuple[Entity, Component, ...]]:
		pass
