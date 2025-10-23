from pygbase.ecs.component import Component


class Query:
	def __init__(self):
		self.of_components: list[type[Component]] = []
		self.with_components: list[type[Component]] = []
		self.without_components: list[type[Component]] = []
