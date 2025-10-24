from pygbase.ecs.component import Component


class Query:
	def __init__(self):
		# Components returned from the query
		self.of_components: list[type[Component]] = []

		# Components that entities in the query have additionally
		self.with_components: list[type[Component]] = []

		# Components that entities in the query must not have
		self.without_components: list[type[Component]] = []
