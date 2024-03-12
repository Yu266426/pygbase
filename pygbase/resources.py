import json
import logging
import os
from collections import deque
from typing import Any, Callable, Optional

from .common import Common


class ResourceType:
	def __init__(self, name: str, container_path: str, file_ending: str, default_data: dict, init_check: Optional[Callable[[dict], bool]], load_resource: Callable[[dict, str], Any]):
		self.name = name

		self.container_path = container_path

		self.file_ending = file_ending

		self.default_data = default_data

		self._init_check = init_check
		self.load_resource = load_resource

	def generate_config(self, config_path: str, file_name: str):
		with open(config_path, "r") as config_file:
			data = json.load(config_file)

		resource_name = file_name[:-4]
		if resource_name not in data:
			resource_data = self.default_data.copy()

			data[resource_name] = resource_data

			with open(config_path, "w") as config_file:
				config_file.write(json.dumps(data))

	def check_init(self, data: dict) -> bool:
		if self._init_check is not None:
			return self._init_check(data)
		else:
			return True


class ResourceManager:
	_resource_types: dict[int, ResourceType] = {}

	_max_load_per_update: int = 1

	_resources_to_load: deque[tuple[int, str, str]] = deque()  # [type_id, path , name]
	_loaded_resources: dict[int, dict[str, Any]] = {}

	@classmethod
	def add_resource_type(cls, type_id, resource_type: ResourceType):
		cls._resource_types[type_id] = resource_type

	@classmethod
	def _init_for_resource(cls, type_id: int, resource_type: ResourceType):
		config_path = os.path.join(resource_type.container_path, "config.json")
		names = set()

		# Create config if it does not exist
		if not os.path.isfile(config_path):
			with open(config_path, "x") as config_file:
				config_file.write(json.dumps({}))

		for dir_path, _, file_names in os.walk(resource_type.container_path):
			for file_name in file_names:
				if file_name.endswith(resource_type.file_ending):
					file_path = os.path.join(dir_path, file_name)

					resource_type.generate_config(config_path, file_name)
					cls._resources_to_load.append((type_id, file_path, file_name[:-4]))

					names.add(file_name[:-4])

		# Reorganise config json
		with open(config_path, "r") as config_file:
			config_data: dict = json.load(config_file)

		data = {key: value for key, value in config_data.items() if key in names}  # Make sure only available files are in config

		keys = list(data.keys())
		keys.sort()

		sorted_data = {key: data[key] for key in keys}

		with open(config_path, "w") as config_file:
			config_file.write(json.dumps(sorted_data, indent=2))

		cls._loaded_resources[type_id] = {}

	@classmethod
	def init_load(cls):
		for type_id, resource_type in cls._resource_types.items():
			cls._init_for_resource(type_id, resource_type)

	@classmethod
	def load_update(cls):
		# If all resources are loaded
		if len(cls._resources_to_load) == 0:
			for type_id, resource_type in cls._resource_types.items():
				logging.info(f"Loaded {len(cls._loaded_resources[type_id])} {resource_type.name}")
			return True

		# Load resources
		else:
			# Only loads max_load_per_update resources per update
			for _ in range(cls._max_load_per_update):
				if len(cls._resources_to_load) > 0:
					# Get resources info
					resource_info = cls._resources_to_load.popleft()

					resource_type_id = resource_info[0]
					resource_type = cls._resource_types[resource_info[0]]
					resource_path = resource_info[1]
					resource_name = resource_info[2]

					logging.debug(f"Loading: {resource_path}")

					with open(os.path.join(resource_type.container_path, "config.json")) as config_file:
						config_data = json.load(config_file)
						data = config_data[resource_name]

					if resource_type.check_init(data):
						cls._loaded_resources[resource_type_id][resource_name] = resource_type.load_resource(data, resource_path)
					else:
						logging.warning(f"Skipping {resource_path}, uninitialized config")

			return False

	@classmethod
	def get_resource(cls, type_name: str, resource_name) -> Any:
		return cls._loaded_resources[Common.get_resource_type(type_name)][resource_name]

	@classmethod
	def get_resources_of_type(cls, type_name: str):
		return cls._loaded_resources[Common.get_resource_type(type_name)]
