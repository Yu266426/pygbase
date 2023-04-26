class Timer:
	def __init__(self, cooldown: float, start_on: bool, repeating: bool):
		self._cooldown = cooldown
		self._repeating = repeating

		self._time = 0 if start_on else cooldown

		self._is_done = start_on

	def set_cooldown(self, cooldown: float):
		self._cooldown = cooldown

	def tick(self, delta: float = 1 / 60):
		self._time -= delta

		if self._repeating:
			self._is_done = False
			if self._time < 0:
				self._time += self._cooldown
				self._is_done = True
		else:
			if self._time < 0:
				self._time = 0
				self._is_done = True

	def start(self):
		self._time = self._cooldown
		self._is_done = False

	def done(self):
		if self._is_done:
			return True
