import enum


class ParticleTypes(enum.Enum):
	DEFAULT = enum.auto()
	PLAYER_ENERGY = enum.auto()


class ParticleOptions(enum.Enum):
	COLOUR = enum.auto()
	SIZE = enum.auto()
	SIZE_DECAY = enum.auto()
	VELOCITY_DECAY = enum.auto()
	GRAVITY = enum.auto()
	EFFECTOR = enum.auto()
