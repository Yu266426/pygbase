from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .component import Component


class Entity:
	default_components: dict[type[Component], tuple[...]] = {}

	def __init__(self, entity_id: int):
		self.id = entity_id
