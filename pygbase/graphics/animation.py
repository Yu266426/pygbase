import pygame

from .image import Image
from ..camera import Camera
from ..resources import ResourceManager


class Animation:
	def __init__(self, sprite_sheet_name: str, anim_start_index: int, length: int, looping=True):
		self.sprite_sheet_id = sprite_sheet_name
		self.anim_start_index = anim_start_index
		self.length = length

		self.looping = looping

		self.frame = 0.0
		self.images: list[Image] = []

		self._load_animation()

	def _load_animation(self):
		for index in range(self.anim_start_index, self.anim_start_index + self.length):
			self.images.append(ResourceManager.get_resource(2, self.sprite_sheet_id).get_image(index))

	def change_frame(self, amount: float):
		self.frame += amount

		if self.frame >= self.length:
			if self.looping:
				self.frame = 0
			else:
				self.frame = self.length - 0.01
		if self.frame < 0:
			if self.looping:
				self.frame = self.length - 0.01
			else:
				self.frame = 0

	def draw_at_pos(self, screen: pygame.Surface, pos: pygame.Vector2, camera: Camera, angle: float = 0, flag: int = 0, draw_pos: str = "topleft"):
		image = self.images[int(self.frame)]

		# TODO: Finish all variations
		if draw_pos == "topleft":
			rect = image.get_image(angle).get_rect(center=image.get_image().get_rect(topleft=pos).center)
		elif draw_pos == "center":
			rect = image.get_image(angle).get_rect(center=image.get_image().get_rect(center=pos).center)
		elif draw_pos == "midbottom":
			rect = image.get_image(angle).get_rect(center=image.get_image().get_rect(midbottom=pos).center)
		else:
			raise ValueError(f"{draw_pos} not a valid position.")

		image.draw(screen, camera.world_to_screen(rect.topleft), angle=angle, special_flags=flag)


class AnimationManager:
	def __init__(self, states: list[tuple[str, Animation, int]], starting_state: str, reset_animation_on_switch: bool = True):
		self.current_state = starting_state
		self.states = {}
		self.animation_info = {}

		for state, animation, animation_speed in states:
			self.states[state] = animation
			self.animation_info[state] = [animation_speed]

		self.reset_animation_on_switch = reset_animation_on_switch

	def switch_state(self, new_state: str):
		if self.current_state != new_state:
			self.current_state = new_state

			if self.reset_animation_on_switch:
				self.states[self.current_state].frame = 0

	def update(self, delta: float):
		self.states[self.current_state].change_frame(self.animation_info[self.current_state][0] * delta)

	def draw_at_pos(self, screen: pygame.Surface, pos: pygame.Vector2, camera: Camera, angle: float = 0, flag=0, draw_pos: str = "topleft"):
		self.states[self.current_state].draw_at_pos(screen, pos, camera, angle=angle, flag=flag, draw_pos=draw_pos)
