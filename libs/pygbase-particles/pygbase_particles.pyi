class ParticleManager:
	def __new__(cls) -> ParticleManager:
		...

	def activate_spawner(self, index: int):
		...

	def deactivate_spawner(self, index: int):
		...

	def add_point_spawner(self,
	                      pos: tuple[float, float],
	                      cooldown: float,
	                      amount: int,
	                      start_active: bool,
	                      radial_vel_range: tuple[float, float] = (0, 0)) -> int:
		...

	def add_particle(self, pos: tuple[float, float], vel: tuple[float, float], vel_decay: float, gravity: tuple[float, float], effector: bool,
	                 size: float, size_decay: float, color: tuple[int, int, int]):
		...

	def update(self, delta: float):
		...

	def get_particle_positions(self) -> list[tuple[float, float]]:
		...

	def get_particle_sizes(self) -> list[float]:
		...

	def get_particle_colors(self) -> list[tuple[int, int, int]]:
		...
