import enum
import logging
from typing import Any


class ParticleOptions(enum.Enum):
	NAME = enum.auto()
	COLOUR = enum.auto()
	SIZE = enum.auto()
	SIZE_DECAY = enum.auto()
	VELOCITY_DECAY = enum.auto()
	GRAVITY = enum.auto()
	EFFECTOR = enum.auto()
	BOUNCE = enum.auto()


class Common:
	_values: dict[str, Any] = {}

	_game_states: dict[str, int] = {"all": 0}

	_resource_types: dict[str, int] = {}

	_particle_settings: dict[str, dict["ParticleOptions", str | list[str] | tuple[float] | bool]] = {
		"default": {
			ParticleOptions.NAME: "default",
			ParticleOptions.COLOUR: ["white"],
			ParticleOptions.SIZE: (4.0, 7.0),
			ParticleOptions.SIZE_DECAY: (3.0, 5.0),
			ParticleOptions.VELOCITY_DECAY: (1.8, 2.2),
			ParticleOptions.GRAVITY: (0, 0),
			ParticleOptions.EFFECTOR: True,
			ParticleOptions.BOUNCE: ((0.0, 0.1), (0.0, 0.1))
		}
	}

	@classmethod
	def set_value(cls, name: str, value: Any) -> None:
		cls._values[name] = value

	@classmethod
	def get_value(cls, name: str) -> Any:
		return cls._values[name]

	@classmethod
	def add_game_state(cls, name: str, game_state_id: int):
		if name not in cls._game_states:
			cls._game_states[name] = game_state_id
		else:
			logging.error(f"Game state name: `{name}` already taken")
			raise KeyError(f"Game state name: `{name}` does not exist")

	@classmethod
	def get_game_state_id(cls, name: str):
		if name in cls._game_states:
			return cls._game_states[name]
		else:
			logging.error(f"Game state name: `{name}` does not exist")
			raise KeyError(f"Game state name: `{name}` does not exist")

	@classmethod
	def add_resource_type(cls, name: str, resource_id: int):
		if name not in cls._resource_types:
			cls._resource_types[name] = resource_id
		else:
			logging.error(f"Resource name: `{name}` already taken")
			raise KeyError(f"Resource name: `{name}` does not exist")

	@classmethod
	def get_resource_type(cls, name: str):
		if name in cls._resource_types:
			return cls._resource_types[name]
		else:
			logging.error(f"Resource name: `{name}` does not exist")
			raise KeyError(f"Resource name: `{name}` does not exist")

	@classmethod
	def add_particle_setting(
			cls,
			name: str,
			colour: list,
			size: tuple[float, float],
			size_decay: tuple[float, float],
			velocity_decay: tuple[float, float],
			gravity: tuple[float, float],
			effector: bool,
			bounce: tuple[tuple[float, float], tuple[float, float]]
	):
		if name not in cls._particle_settings:
			cls._particle_settings[name] = {
				ParticleOptions.NAME: name,
				ParticleOptions.COLOUR: colour,
				ParticleOptions.SIZE: size,
				ParticleOptions.SIZE_DECAY: size_decay,
				ParticleOptions.VELOCITY_DECAY: velocity_decay,
				ParticleOptions.GRAVITY: gravity,
				ParticleOptions.EFFECTOR: effector,
				ParticleOptions.BOUNCE: bounce
			}
		else:
			logging.warning(f"Particle setting name: `{name}` already taken")

	@classmethod
	def get_particle_setting(cls, name: str) -> dict[ParticleOptions, list[str] | tuple[float] | bool]:
		if name in cls._particle_settings:
			return cls._particle_settings[name]
		else:
			logging.warning(f"Particle setting name: `{name}` does not exist. Using default settings.")
			return cls._particle_settings["default"]
