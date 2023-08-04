from collections.abc import Callable

import pygame

from .text import Text
from .ui_elements import Button, Frame
from .ui_manager import UIManager
from .values import UIValue
from ..common import Common
from ..timer import Timer


class DialogueNode:
	def __init__(self, name: str, message: str):
		self.name = name
		self.message: str = message

		self.words: list[str] = self.message.split(" ")
		self.texts: list[Text] = []  # Will be set when processed through DialogueManager

		self.current_word = 0
		self.current_char = 0

		self.finished_displaying = False
		self.just_finished_displaying = False

	def process_message(self, starting_y: float, width: int, word_gap: float):
		# Generate text objects
		self.texts.clear()

		for word in self.words:
			self.texts.append(Text((0, starting_y), "arial", 30, "white", text=word, use_sys=True))

		# Position words
		for index in range(1, len(self.texts)):
			current_text = self.texts[index]
			previous_text = self.texts[index - 1]

			current_text.pos.update(previous_text.text_rect.right + word_gap, previous_text.text_rect.top)
			current_text.reposition()

			if current_text.text_rect.right > width:
				current_text.pos.x = 0
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

			self.texts[self.current_word].set_text(self.words[self.current_word][:self.current_char])
		else:
			self.just_finished_displaying = False

	def draw(self, surface: pygame.Surface):
		for text in self.texts:
			text.draw(surface)


class DialogueOption:
	def __init__(self, response: str, next_node: str = "", callback: Callable[[...], None] = None, callback_args: tuple = ()):
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

		self.width = 0.7 * Common.get_value("screen_width")
		self.height = 0.4 * Common.get_value("screen_height")
		self.starting_y = Common.get_value("screen_height") - self.height

		self.word_gap = word_gap

		self.char_timer = Timer(char_timing, False, True)

		self.ui_manager = UIManager()
		self.text_background = self.ui_manager.add_frame(Frame(
			(UIValue(0), UIValue(0.6, False)),
			(UIValue(1, False), UIValue(0.4, False)),
			self.ui_manager.base_container,
			bg_colour=(20, 20, 20, 50)
		))

		self.option_frame = self.ui_manager.add_frame(Frame(
			(UIValue(0.75, False), UIValue(0.6, False)),
			(UIValue(0.25, False), UIValue(0.4, False)),
			self.ui_manager.base_container,
			bg_colour=(50, 50, 50, 100)
		))

	def get_current_node(self) -> DialogueNode | None:
		if self.current_node == "":
			return None

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
			self.option_frame.clear()

			self.get_current_node().process_message(self.starting_y, self.width, self.word_gap)
			self.char_timer.start()

	def option_callback(self, option: DialogueOption):
		self.set_current_node(option.selected())
		self.option_frame.clear()

	def generate_options(self):
		options = self.get_options()
		if len(options) == 0:
			self.option_frame.add_element(Button(
				(UIValue(0), UIValue(0)), (UIValue(1, False), UIValue(0)),
				"image", "button",
				self.option_frame,
				self.option_callback, callback_args=(DialogueOption("Dismiss"),),
				text="Dismiss"
			))
		else:
			for option in self.get_options():
				self.option_frame.add_element(Button(
					(UIValue(0), UIValue(0)), (UIValue(1, False), UIValue(0)),
					"image", "button",
					self.option_frame,
					self.option_callback, callback_args=(option,),
					text=option.response
				))

	def update(self, delta: float):
		self.ui_manager.update(delta)

		if self.get_current_node() is not None:
			self.char_timer.tick(delta)

			if self.char_timer.just_done():
				self.get_current_node().next_char()

				if self.get_current_node().just_finished_displaying:
					self.generate_options()

	def draw(self, surface: pygame.Surface):
		if self.get_current_node() is not None:
			self.ui_manager.draw(surface)

			self.get_current_node().draw(surface)
