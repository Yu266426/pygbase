from collections.abc import Callable

import pygame

from .ui_element import Frame
from .ui_elements import Button, Image, Text
from .values import YAlign, Padding, Grow, Layout, XAlign, Fit
from ..common import Common
from ..timer import Timer
from .rawtext import RawText


class DialogueNode:
	def __init__(self, name: str, message: str):
		self.name = name
		self.message: str = message

		self.words: list[str] = self.message.split(" ")
		self.texts: list[RawText] = []  # Will be set when processed through DialogueManager

		self.current_word = 0
		self.current_char = 0

		self.finished_displaying = False
		self.just_finished_displaying = False

	def process_message(self, starting_x: float, starting_y: float, width: int, word_gap: float):
		# Generate text objects
		self.texts.clear()

		for word in self.words:
			self.texts.append(RawText((starting_x, starting_y), "arial", 30, "white", text=word, use_sys=True))

		# Position words
		for index in range(1, len(self.texts)):
			current_text = self.texts[index]
			previous_text = self.texts[index - 1]

			current_text.pos.update(
				previous_text.text_rect.right + word_gap, previous_text.text_rect.top
			)
			current_text.reposition()

			if current_text.text_rect.right > width:
				current_text.pos.x = starting_x
				current_text.pos.y += previous_text.text_rect.height
				current_text.reposition()

		# Reset words
		for text in self.texts:
			text.set_text("")

		# Reset Display:
		self.current_word = 0
		self.current_char = 0
		self.finished_displaying = False

	def next_char(self):
		if not self.finished_displaying:
			self.current_char += 1
			if self.current_char > len(self.words[self.current_word]):
				self.current_word += 1
				self.current_char = 0

			if self.current_word >= len(self.words):
				self.finished_displaying = True
				self.just_finished_displaying = True
				return

			self.texts[self.current_word].set_text(
				self.words[self.current_word][: self.current_char]
			)
		else:
			self.just_finished_displaying = False

	def draw(self, surface: pygame.Surface):
		for text in self.texts:
			text.draw(surface)


class DialogueOption:
	def __init__(
			self,
			response: str,
			next_node: str = "",
			callback: Callable[..., None] | None = None,
			callback_args: tuple = (),
	):
		self.response = response
		self.next_node = next_node
		self.callback = callback
		self.callback_args = callback_args

	def selected(self) -> str:
		if self.callback is not None:
			self.callback(*self.callback_args)

		return self.next_node


class DialogueManager:
	def __init__(self, word_gap: float, char_timing: float):
		self.current_node = ""
		self.nodes: dict[str, DialogueNode] = {}
		self.options: dict[str, list[DialogueOption]] = {}

		self.word_gap = word_gap

		self.char_timer = Timer(char_timing, False, True)

		self.ui = None
		self.width = None
		self.height = None
		self.starting_y = None
		self._make_ui()

	def option_callback(self, option: DialogueOption):
		self.set_current_node(option.selected())
		self._make_ui()

	def _make_ui(self):
		with Frame(size=(Grow(), Grow()), padding=Padding.all(10), layout=Layout.TOP_TO_BOTTOM) as ui:
			Frame(size=(Grow(), Grow(2)))  # Padding

			with Frame(size=(Grow(), Grow()), padding=Padding.all(6), bg_color=(20, 20, 20, 50)):
				text_frame = Frame(size=(Grow(4), Grow()))

				with Frame(size=(Grow(), Grow()), layout=Layout.TOP_TO_BOTTOM, bg_color=(50, 50, 50, 100)):  # Option Frame
					self._generate_options()

		ui.resolve_layout(Common.get("screen_size"))
		self.ui = ui
		self.width = text_frame.width
		self.height = text_frame.height
		self.starting_x = text_frame.x
		self.starting_y = text_frame.y

	def _generate_options(self):
		options = self.get_options()
		if len(options) == 0:
			with Button(
					self.option_callback,
					size=(Grow(), Fit()),
					callback_args=(DialogueOption("Dismiss"),),
			):
				with Image(
						image="image/button",
						size=(Grow(), Fit()),
						x_align=XAlign.CENTER,
						y_align=YAlign.CENTER,
				):
					Text("dismiss", 30, "white")

		else:
			for option in self.get_options():
				with Button(
						self.option_callback,
						callback_args=(option,),
						size=(Grow(), Fit()),
				):
					with Image(
							image="image/button",
							size=(Grow(), Fit()),
							x_align=XAlign.CENTER,
							y_align=YAlign.CENTER,
					):
						Text(option.response, 30, "white")

	def has_current_node(self) -> bool:
		return self.current_node in self.nodes

	def get_current_node(self) -> DialogueNode:
		return self.nodes[self.current_node]

	def get_options(self) -> list[DialogueOption]:
		if self.current_node not in self.options:
			return []

		return self.options[self.current_node]

	def add_node(self, node: DialogueNode) -> "DialogueManager":
		self.nodes[node.name] = node
		return self

	def add_option(self, node_name: str, option: DialogueOption) -> "DialogueManager":
		if node_name not in self.options:
			self.options[node_name] = []

		self.options[node_name].append(option)
		return self

	def set_current_node(self, node_name: str):
		self.current_node = node_name
		if self.current_node != "":
			self._make_ui()

			self.get_current_node().process_message(self.starting_x, self.starting_y, self.width, self.word_gap)
			self.char_timer.start()

	def update(self, delta: float):
		self.ui.update(delta)

		if self.has_current_node():
			self.char_timer.tick(delta)

			if self.char_timer.just_done():
				self.get_current_node().next_char()

				if self.get_current_node().just_finished_displaying:
					self._make_ui()

	def draw(self, surface: pygame.Surface):
		if self.has_current_node():
			self.ui.draw(surface)

			self.get_current_node().draw(surface)
