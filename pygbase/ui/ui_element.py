import logging
from collections import deque
from types import TracebackType
from typing import Self, Type, Any, Callable

import pygame

from ..debug import Debug
from .values import Fit, Layout, Grow, Padding, XAlign, YAlign, EPSILON, UIActionTriggers
from .. import Input, Common


class Frame:
	"""
	Base class for UI elements with layout capabilities.

	Handles positioning, sizing and layout of UI elements in a hierarchical structure.
	"""

	# For debugging purposes
	ID: str = "frame"

	element_stack: deque[Self] = deque()

	def __init__(
			self,
			pos: tuple[float, float] = (0, 0),
			size: tuple[float | Fit | Grow, float | Fit | Grow] = (Fit(), Fit()),
			layout: Layout = Layout.LEFT_TO_RIGHT,
			padding: Padding = Padding(),
			gap: float = 0,
			x_align: XAlign = XAlign.LEFT,
			y_align: YAlign = YAlign.TOP,
			bg_color: pygame.typing.ColorLike = (0, 0, 0, 0),
			can_interact: bool = False,
			blocks_mouse: bool = False,
	):
		self._pos = pygame.Vector2(pos)
		self._resolved_pos = pygame.Vector2(pos)

		width = 0 if isinstance(size[0], (Fit, Grow)) else size[0]
		height = 0 if isinstance(size[1], (Fit, Grow)) else size[1]

		min_width = size[0].min if isinstance(size[0], (Fit, Grow)) else size[0]
		min_height = size[1].min if isinstance(size[1], (Fit, Grow)) else size[1]

		max_width = size[0].max if isinstance(size[0], (Fit, Grow)) else size[0]
		max_height = size[1].max if isinstance(size[1], (Fit, Grow)) else size[1]

		self._size = pygame.Vector2(width, height)
		self._min_size = pygame.Vector2(min_width, min_height)
		self._max_size = pygame.Vector2(max_width, max_height)

		self._resolved_size = self._size.copy()
		self._iter_min_size = self._min_size.copy()
		self._resolved_min_size = pygame.Vector2(0, 0)
		self.size_settings = size

		self.direction = layout
		self.padding = padding
		self.child_gap = gap

		self.x_alignment = x_align
		self.y_alignment = y_align

		self.background_color = bg_color

		self.children: list["Frame"] = []

		self.current_resolve_size = (0, 0)
		self.dirty = True
		self._is_base = False

		self._prev_resolved_pos = pygame.Vector2(-1, -1)
		self._prev_resolved_size = pygame.Vector2(-1, -1)
		self._prev_resolved_min_size = pygame.Vector2(-1, -1)

		self.parent: Frame | None = self.element_stack[-1] if len(self.element_stack) > 0 else None
		if self.parent is not None:
			self.parent.children.append(self)  # NoQA: Dunno why pycharm thinks this is wrong

		# Surface
		self._surface: pygame.Surface | None = None

		# UI actions
		self._time: float = 0  # TODO: Use multiple times for different actions?
		self.can_interact: bool = can_interact
		self.blocks_mouse: bool = blocks_mouse

		self._hovered: bool = False
		self._clicked: bool = False

		self._actions: dict[UIActionTriggers, list[tuple[Callable[..., None], tuple]]] = {
			trigger: [] for trigger in UIActionTriggers
		}  # TODO: Change to have list of preset actions. Callables would be an action with input of a Callable

		self._timed_actions: dict[int, list[UIActionTriggers]] = {}  # TODO: Use in some way?

	@property
	def size(self) -> pygame.Vector2:
		return self._resolved_size

	# TODO: Rework so setting these will trigger a layout recalculation
	@property
	def pos(self) -> tuple[float, float]:
		return self._resolved_pos.x, self._resolved_pos.y

	@property
	def x(self) -> float:
		return self._resolved_pos.x

	@x.setter
	def x(self, value: float):
		self._resolved_pos.x = value

	@property
	def y(self) -> float:
		return self._resolved_pos.y

	@y.setter
	def y(self, value: float):
		self._resolved_pos.y = value

	@property
	def _draw_pos(self):
		if self.parent is not None:
			return self._resolved_pos - self.parent._resolved_pos
		else:
			return self.pos

	@property
	def width(self) -> float:
		return self._resolved_size.x

	@width.setter
	def width(self, value: float):
		self._resolved_size.x = value

	@property
	def min_width(self) -> float:
		return self._resolved_min_size.x

	@min_width.setter
	def min_width(self, value: float):
		self._resolved_min_size.x = value

	@property
	def height(self) -> float:
		return self._resolved_size.y

	@height.setter
	def height(self, value: float):
		self._resolved_size.y = value

	@property
	def min_height(self) -> float:
		return self._resolved_min_size.y

	@min_height.setter
	def min_height(self, value: float):
		self._resolved_min_size.y = value

	@property
	def rect(self) -> pygame.FRect:
		return pygame.FRect(self.pos, self.size)

	def __enter__(self) -> Self:
		self.element_stack.append(self)
		return self

	def __exit__(
			self, exc_type: Type | None, exc_value: Any | None, traceback: TracebackType | None
	) -> bool:
		if exc_type is not None:
			logging.error(f"Exception raised {exc_value}")
			return False  # True -> Suppress exception

		self.element_stack.pop()

		# If empty, then this is the parent element
		if len(self.element_stack) == 0:
			self.resolve_layout(Common.get("screen_size"))
			self._is_base = True

		return False

	def resolve_layout(self, size: tuple[float, float]) -> tuple[float, float]:
		"""
		Iterative layout resolution.
		Wrap the layout passes in a loop until the layout converges.
		"""
		self.current_resolve_size = size

		# Create a temporary root frame to act as a container for self.
		root = Frame(size=size)
		root._resolved_size = root._size.copy()
		root.children.append(self)
		self.parent = root

		iterations = 0
		max_iterations = 8  # Safeguard to prevent infinite loops

		while iterations < max_iterations:
			root._propagate_dirtiness()

			if not root.dirty:
				break

			# print("Iter:", iterations)

			# Reset the entire tree (both root and all its children)
			first_reset = iterations == 0
			root._iter_reset_resolved_values(first_reset)

			# Run layout passes
			root._resolve_x_sizing()
			root._grow_children_x()
			root._shrink_children_x()
			root._wrap_text()
			root._resolve_y_sizing()
			root._grow_children_y()
			root._shrink_children_y()
			root._resolve_position()

			iterations += 1

		if iterations >= max_iterations:
			logging.warning("Warning: Layout did not converge after maximum iterations.")

		self.parent = None  # Detach from temporary root
		return self.min_width, self.min_height

	def _propagate_dirtiness(self):
		for child in self.children:
			self.dirty |= child._propagate_dirtiness()

		# print("Dirt:", self.background_color, self.dirty, end=" |	")
		# print(
		# 	self._prev_resolved_pos,
		# 	self._resolved_pos,
		# 	"|",
		# 	self._prev_resolved_size,
		# 	self._resolved_size,
		# 	"|",
		# 	self._prev_resolved_min_size,
		# 	self._resolved_min_size,
		# )

		self.dirty |= (
				(self._prev_resolved_pos - self._resolved_pos).length_squared() > EPSILON
				or (self._prev_resolved_size - self._resolved_size).length_squared() > EPSILON
				or (self._prev_resolved_min_size - self._resolved_min_size).length_squared() > EPSILON
		)

		return self.dirty

	def _iter_reset_resolved_values(self, first_reset: bool):
		# print(self.background_color, (self.min_width, self.min_height), self.size)

		self._prev_resolved_pos = self._resolved_pos.copy()
		self._prev_resolved_size = self._resolved_size.copy()
		self._prev_resolved_min_size = self._resolved_min_size.copy()

		if first_reset:
			self._iter_min_size = self._min_size.copy()

		self._resolved_pos.update(self._pos)
		self._resolved_size.update(self._size)
		self._resolved_min_size.update(self._iter_min_size)

		self.dirty = False

		for child in self.children:
			child._iter_reset_resolved_values(first_reset)

	def _resolve_x_sizing(self):
		# Bottom up pass (Post order DFS)
		# Let children resolve sizing first
		for child in self.children:
			child._resolve_x_sizing()

		self.min_width = max(self._iter_min_size.x, self.min_width)

		# Resolve sizing
		parent = self.parent
		if parent is None:
			return

		padding = self.padding

		# Add padding and child gaps
		child_gap = (len(self.children) - 1) * self.child_gap

		self_x_not_fixed = isinstance(self.size_settings[0], (Fit, Grow))
		parent_x_not_fixed = isinstance(parent.size_settings[0], (Fit, Grow))

		if self_x_not_fixed:
			self.width += padding.left + padding.right

			self.min_width += padding.left + padding.right

			if self.direction == Layout.LEFT_TO_RIGHT:
				self.width += child_gap
				self.min_width += child_gap

		self.width = pygame.math.clamp(self.width, self.min_width, self._max_size.x)

		# Add child sizes
		if parent.direction == Layout.LEFT_TO_RIGHT:
			if parent_x_not_fixed:
				parent.width += self.width
				parent.min_width += self.min_width

		elif parent.direction == Layout.TOP_TO_BOTTOM:
			if parent_x_not_fixed:
				parent.width = max(parent.width, self.width)
				parent.min_width = max(parent.min_width, self.min_width)

		# print(
		# 	self.background_color,
		# 	" -> ",
		# 	parent.background_color,
		# 	parent._iter_min_size.x,
		# 	parent.min_width,
		# )
		pass

	def _resolve_y_sizing(self):
		# Bottom up pass (Post order DFS)
		# Let children resolve sizing first
		for child in self.children:
			child._resolve_y_sizing()

		self.min_height = max(self._iter_min_size.y, self.min_height)

		# Resolve sizing
		parent = self.parent
		if parent is None:
			return

		padding = self.padding

		# Add padding and child gaps
		child_gap = (len(self.children) - 1) * self.child_gap

		self_y_not_fixed = isinstance(self.size_settings[1], (Fit, Grow))
		parent_y_not_fixed = isinstance(parent.size_settings[1], (Fit, Grow))

		if self_y_not_fixed:
			self.height += padding.top + padding.bottom

			self.min_height += padding.top + padding.bottom

			if self.direction == Layout.TOP_TO_BOTTOM:
				self.height += child_gap

				self.min_height += child_gap

		self.height = pygame.math.clamp(self.height, self.min_height, self._max_size.y)

		# Add child sizes
		new_parent_min_height = parent._iter_min_size.y
		if parent.direction == Layout.LEFT_TO_RIGHT:
			if parent_y_not_fixed:
				parent.height = max(parent.height, self.height)
				new_parent_min_height = max(new_parent_min_height, self.min_height)

		elif parent.direction == Layout.TOP_TO_BOTTOM:
			if parent_y_not_fixed:
				parent.height += self.height
				new_parent_min_height += self.min_height

		parent.min_height = max(parent.min_height, new_parent_min_height)

	def _grow_children_x(self):
		# Calculate available space
		remaining_width = self.width - self.padding.left - self.padding.right
		children_gap = (len(self.children) - 1) * self.child_gap

		if self.direction == Layout.LEFT_TO_RIGHT:
			grow_children = [
				child for child in self.children if isinstance(child.size_settings[0], Grow)
			]

			# Subtract children and gaps
			remaining_width -= sum(child.size.x for child in self.children) + children_gap

			while remaining_width > EPSILON and len(grow_children) > 0:
				min_ratio = grow_children[0].width / grow_children[0].size_settings[0].weight
				second_min_ratio = float("inf")

				# Find min and second_min ratios
				for child in grow_children:
					ratio = child.width / child.size_settings[0].weight

					if ratio < min_ratio:
						second_min_ratio = min_ratio
						min_ratio = ratio

					elif ratio > min_ratio:
						second_min_ratio = min(second_min_ratio, ratio)

				total_weight = 0
				for child in grow_children:
					child_weight = child.size_settings[0].weight
					ratio = child.width / child.size_settings[0].weight

					if ratio == min_ratio:
						total_weight += child_weight

				for child in grow_children:
					child_weight = child.size_settings[0].weight
					ratio = child.width / child_weight

					target_width = second_min_ratio * child_weight
					if ratio == min_ratio:
						prev_width = child.width

						width_to_add = min(
							target_width, remaining_width / total_weight * child_weight
						)
						child.width += width_to_add

						if child.width > child._max_size.x:
							child.width = child._max_size.x
							grow_children.remove(child)

						remaining_width -= child.width - prev_width

		if self.direction == Layout.TOP_TO_BOTTOM:
			for child in self.children:
				if isinstance(child.size_settings[0], Grow):
					child.width += remaining_width - child.width
					child.width = pygame.math.clamp(child.width, child.min_width, child._max_size.x)

		for child in self.children:
			child._grow_children_x()

	# print(self.background_color, self.width, self.min_width, self._max_size.x)

	def _grow_children_y(self):
		# Calculate available space
		remaining_height = self.height - self.padding.top - self.padding.bottom
		children_gap = (len(self.children) - 1) * self.child_gap

		if self.direction == Layout.LEFT_TO_RIGHT:
			for child in self.children:
				if isinstance(child.size_settings[1], Grow):
					child.height += remaining_height - child.height
					child.height = pygame.math.clamp(
						child.height, child.min_height, child._max_size.y
					)

		if self.direction == Layout.TOP_TO_BOTTOM:
			grow_children = [
				child for child in self.children if isinstance(child.size_settings[1], Grow)
			]

			# Subtract children and gaps
			remaining_height -= sum(child.size.y for child in self.children) + children_gap

			while remaining_height > EPSILON and len(grow_children) > 0:
				min_ratio = grow_children[0].height / grow_children[0].size_settings[1].weight
				second_min_ratio = float("inf")

				# Find min and second_min ratios
				for child in grow_children:
					ratio = child.height / child.size_settings[1].weight

					if ratio < min_ratio:
						second_min_ratio = min_ratio
						min_ratio = ratio

					elif ratio > min_ratio:
						second_min_ratio = min(second_min_ratio, ratio)

				total_weight = 0
				for child in grow_children:
					child_weight = child.size_settings[1].weight
					ratio = child.height / child.size_settings[1].weight

					if ratio == min_ratio:
						total_weight += child_weight

				for child in grow_children:
					child_weight = child.size_settings[1].weight
					ratio = child.height / child_weight

					target_height = second_min_ratio * child_weight
					if ratio == min_ratio:
						prev_height = child.height

						height_to_add = min(
							target_height, remaining_height / total_weight * child_weight
						)
						child.height += height_to_add

						if child.height > child._max_size.y:
							child.height = child._max_size.y
							grow_children.remove(child)

						remaining_height -= child.height - prev_height

		for child in self.children:
			child._grow_children_y()

	def _shrink_children_x(self):
		remaining_width = self.width - self.padding.left - self.padding.right
		children_gap = (len(self.children) - 1) * self.child_gap

		if self.direction == Layout.LEFT_TO_RIGHT:
			shrink_children = [
				child for child in self.children if isinstance(child.size_settings[0], (Grow, Fit))
			]

			remaining_width -= sum(child.size.x for child in self.children) + children_gap

			while remaining_width < -EPSILON and len(shrink_children) > 0:
				largest = shrink_children[0].width
				second_largest = 0

				width_to_subtract = remaining_width

				for child in shrink_children:
					if child.width > largest:
						second_largest = largest
						largest = child.width

					elif child.width < largest:
						second_largest = max(second_largest, child.width)
						width_to_subtract = second_largest - largest

				width_to_subtract = max(width_to_subtract, remaining_width / len(shrink_children))

				for child in shrink_children:
					prev_width = child.width
					if child.width == largest:
						child.width += width_to_subtract  # width_to_subtract is negative

						if child.width < child.min_width:
							child.width = child.min_width
							shrink_children.remove(child)

						remaining_width -= child.width - prev_width  # remaining_width is negative

		elif self.direction == Layout.TOP_TO_BOTTOM:
			shrink_children = [
				child for child in self.children if isinstance(child.size_settings[0], (Grow, Fit))
			]

			for child in shrink_children:
				child.width = min(child.width, remaining_width)
				child.width = pygame.math.clamp(child.width, child.min_width, child._max_size.x)

		for child in self.children:
			child._shrink_children_x()

	def _shrink_children_y(self):
		remaining_height = self.height - self.padding.top - self.padding.bottom
		children_gap = (len(self.children) - 1) * self.child_gap

		if self.direction == Layout.LEFT_TO_RIGHT:
			shrink_children = [
				child for child in self.children if isinstance(child.size_settings[1], (Grow, Fit))
			]

			for child in shrink_children:
				child.height = min(child.height, remaining_height)
				child.height = pygame.math.clamp(child.height, child.min_height, child._max_size.y)

		elif self.direction == Layout.TOP_TO_BOTTOM:
			shrink_children = [
				child for child in self.children if isinstance(child.size_settings[1], (Grow, Fit))
			]

			remaining_height -= sum(child.size.y for child in self.children) + children_gap

			while remaining_height < -EPSILON and len(shrink_children) > 0:
				largest = shrink_children[0].height
				second_largest = 0

				height_to_subtract = remaining_height

				for child in shrink_children:
					if child.height > largest:
						second_largest = largest
						largest = child.height

					elif child.height < largest:
						second_largest = max(second_largest, child.height)
						height_to_subtract = second_largest - largest

				height_to_subtract = max(
					height_to_subtract, remaining_height / len(shrink_children)
				)

				for child in shrink_children:
					prev_height = child.height
					if child.height == largest:
						child.height += height_to_subtract  # height_to_subtract is negative

						if child.height < child.min_height:
							child.height = child.min_height
							shrink_children.remove(child)

						remaining_height -= (
								child.height - prev_height
						)  # remaining_height is negative

		for child in self.children:
			child._shrink_children_y()

	def _wrap_text(self):
		# Extended by text child
		for child in self.children:
			child._wrap_text()

	def _resolve_position(self):
		remaining_width = self.width - self.padding.left - self.padding.right
		remaining_height = self.height - self.padding.top - self.padding.bottom
		children_gap = (len(self.children) - 1) * self.child_gap

		x_axis = self.direction == Layout.LEFT_TO_RIGHT

		offset = self.padding.left if x_axis else self.padding.top

		# Add alignment
		if x_axis:
			remaining_width -= sum(child.size.x for child in self.children) + children_gap

			if self.x_alignment == XAlign.CENTER:
				offset += remaining_width / 2
			elif self.x_alignment == XAlign.RIGHT:
				offset += remaining_width
		else:
			remaining_height -= sum(child.size.y for child in self.children) + children_gap

			if self.y_alignment == YAlign.CENTER:
				offset += remaining_height / 2
			elif self.y_alignment == YAlign.BOTTOM:
				offset += remaining_height

		for child in self.children:
			child._resolved_pos = self._resolved_pos + child._pos

			if x_axis:
				child.x += offset
				child.y += self.padding.top

				# Align each child individually
				child_remaining_height = remaining_height - child.height
				if self.y_alignment == YAlign.CENTER:
					child.y += child_remaining_height / 2
				elif self.y_alignment == YAlign.BOTTOM:
					child.y += child_remaining_height
			else:
				child.y += offset
				child.x += self.padding.left

				# Alignment
				child_remaining_width = remaining_width - child.width
				if self.x_alignment == XAlign.CENTER:
					child.x += child_remaining_width / 2
				if self.x_alignment == XAlign.RIGHT:
					child.x += child_remaining_width

			offset += (child.size.x if x_axis else child.size.y) + self.child_gap

		for child in self.children:
			child._resolve_position()

	def add_action(
			self, trigger: UIActionTriggers, action: Callable[..., None], action_args: tuple = ()
	) -> Self:
		self._actions[trigger].append((action, action_args))
		return self

	def _perform_action(self, trigger: UIActionTriggers):
		if self.can_interact:
			for action in self._actions[trigger]:
				action[0](*action[1])

	def update(self, delta: float):
		# Check if ui needs to re-resolve only on the base element
		if self._is_base:
			self._propagate_dirtiness()
			if self.dirty:
				self.resolve_layout(self.current_resolve_size)

		for child in self.children:
			child.update(delta)

		self._time += delta

		if self.can_interact and self.rect.collidepoint(pygame.mouse.get_pos()):
			if not self._hovered:
				self._hovered = True
				self._perform_action(UIActionTriggers.ON_HOVER_ENTER)

				self._time = 0

			if Input.mouse_just_pressed(0, consume=self.blocks_mouse):
				self._clicked = True
				self._perform_action(UIActionTriggers.ON_CLICK_DOWN)

			if Input.mouse_pressed(0, consume=self.blocks_mouse):
				self._perform_action(UIActionTriggers.ON_CLICK_HOLD)

				self._time = 0

			if Input.mouse_just_released(0, consume=self.blocks_mouse):
				self._clicked = False
				self._perform_action(UIActionTriggers.ON_CLICK_UP)

				self._time = 0

			# Consume mouse for now:
			# TODO: Improve by hooking these into actual events
			if self.blocks_mouse:
				for i in range(1, 3):
					Input.mouse_just_pressed(i, consume=self.blocks_mouse)
					Input.mouse_pressed(i, consume=self.blocks_mouse)
					Input.mouse_just_released(i, consume=self.blocks_mouse)

			scroll_y = Input.mouse_scroll_y()
			if scroll_y != 0:
				self._perform_action(UIActionTriggers.ON_SCROLL_Y)
		else:
			if self._hovered:
				self._hovered = False
				self._perform_action(UIActionTriggers.ON_HOVER_EXIT)

				self._time = 0

			if self._clicked:
				self._clicked = False

				self._time = 0

	def _draw_self(self, surface: pygame.Surface):
		"""Drawn on parent"""
		pass

	def _draw_overlay(self, surface: pygame.Surface):
		"""Drawn on self"""
		pass

	def draw(self, surface: pygame.Surface):
		if self._surface is None or self.size != self._surface.size:
			self._surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)

		self._surface.fill(self.background_color)

		self._draw_self(surface)

		# Debug Outline
		Debug.draw_rect(self.rect, "white", width=1)

		for child in self.children:
			child.draw(self._surface)

		self._draw_overlay(self._surface)

		surface.blit(self._surface, self._draw_pos)
