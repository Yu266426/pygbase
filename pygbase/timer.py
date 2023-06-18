class Timer:
	def __init__(self, cooldown: float, start_done: bool, repeating: bool):
		self._cooldown = cooldown
		self._repeating = repeating

		self._time = 0 if start_done else cooldown

		self._is_done = start_done
		self._is_just_done = start_done

	def set_cooldown(self, cooldown: float):
		self._cooldown = cooldown

	def tick(self, delta: float = 1 / 60):
		self._time -= delta

		if self._repeating:
			self._is_done = False
			self._is_just_done = False

			if self._time < 0:
				self._time += self._cooldown
				self._is_done = True
				self._is_just_done = True
		else:
			if self._time < 0:
				if self._is_done:
					self._is_just_done = False
				else:
					self._is_done = True
					self._is_just_done = True

				self._time = 0

	def start(self):
		self._time = self._cooldown
		self._is_done = False
		self._is_just_done = False

	def done(self):
		return self._is_done

	def just_done(self):
		return self._is_just_done
