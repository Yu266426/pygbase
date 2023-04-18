from typing import Any


class Common:
	_values: dict[str, Any] = {}

	# TODO: Add more attributes that store info
	# Eg: particle_settings, with custom method to add / extract

	@classmethod
	def set_value(cls, name: str, value: Any) -> None:
		cls._values[name] = value

	@classmethod
	def get_value(cls, name: str) -> Any:
		return cls._values[name]
