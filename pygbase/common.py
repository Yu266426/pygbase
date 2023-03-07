from typing import Any


class Common:
	_values: dict[str, Any] = {}

	@classmethod
	def set_value(cls, name: str, value: Any) -> None:
		cls._values[name] = value

	@classmethod
	def get_value(cls, name: str) -> Any:
		return cls._values[name]
