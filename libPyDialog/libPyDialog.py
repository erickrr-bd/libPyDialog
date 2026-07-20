"""
Author: Erick Roberto Rodriguez Rodriguez
Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com
GitHub: https://github.com/erickrr-bd/libPyDialog
libPyDialog v2.3.1 - July 2026
Python library that enhances the use of pythondialog to build TUI-type graphical interfaces on terminals.
"""
from pathlib import Path
from dialog import Dialog
from re import compile, match
from libPyUtils import libPyUtils
from dataclasses import dataclass

@dataclass
class libPyDialog:

	python_dialog: Dialog

	def __init__(self, backtitle: str):
		"""
		Class constructor.

		Parameters:
			backtitle (str): Text displayed in the background.
		"""
		self.python_dialog = Dialog(dialog = "dialog")
		self.python_dialog.set_background_title(backtitle)


	def create_message(self, text: str, height: int, width: int, title: str) -> None:
		"""
		Method that displays a message.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
		"""
		self.python_dialog.msgbox(text = text, height = height, width = width, title = title)


	def create_menu(self, text: str, height: int, width: int, choices: tuple, title: str) -> str:
		"""
		Method that creates a menu.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
			choices (tuple): Tuple with the menu options.	
			title (str): Title to display in the box.

		Returns:
			tag (str): Option chosen from the menu.
		"""
		code, tag = self.python_dialog.menu(text = text, height = height, width = width, menu_height = len(choices), choices = choices, title = title)
		if code == self.python_dialog.OK:
			return tag
		elif code == self.python_dialog.CANCEL:
			raise KeyboardInterrupt("Exit")


	def create_form(self, text: str, elements: tuple, height: int, width: int, title: str) -> list:
		"""
		Method that creates a form.

		Parameters:
			text (str): Text to display in the box.
			elements (tuple): Sequence describing the labels and fields.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.

		Returns:
			tag (list): List with the data entered in the form.
		"""
		while True:
			code, tag = self.python_dialog.form(text = text, elements = elements, height = height, width = width, form_height = len(elements), title = title)
			if code == self.python_dialog.OK:
				is_valid = True
				for value in tag:
					if value.strip() == "":
						self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
						is_valid = False
						break
					if len(value) > 100:
						self.create_message("\nInvalid data. Size exceeded (100 characters).", 8, 50, "Error Message")
						is_valid = False
						break
				if is_valid:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_url_form(self, text: str, elements: tuple, height: int, width: int, title: str) -> list:
		"""
		Method that creates a form to enter URLs (URL:PORT format).

		Parameters:
			text (str): Text to display in the box.
			elements (tuple): Sequence describing the labels and fields.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.

		Returns:
			tag (list): List with the data entered in the form.
		"""
		url_regex = r'https?://(?:[a-zA-Z0-9.-]+|\d{1,3}(?:\.\d{1,3}){3}):\d+'

		while True:
			code, tag = self.python_dialog.form(text = text, elements = elements, height = height, width = width, form_height = len(elements), title = title)
			if code == self.python_dialog.OK:
				is_valid = True
				for value in tag:
					if value.strip() == "":
						self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
						is_valid = False
						break
					if len(value) > 100:
						self.create_message("\nInvalid data. Size exceeded (100 characters).", 8, 50, "Error Message")
						is_valid = False
						break
					if not match(url_regex, value):
						self.create_message("\nInvalid data. Required value (URL).", 7, 50, "Error Message")
						is_valid = False
						break
				if is_valid:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_file(self, filepath: str, height: int, width: int, title: str, extensions_list: list) -> str:
		"""
		Method that creates a file selection box.

		Parameters:
			filepath (str): Initial path.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
			extensions_list  (list): List of allowed extensions.

		Returns:
			tag (str): Selected file (path).
		"""
		while True:
			code, tag = self.python_dialog.fselect(filepath = filepath, height = height, width = width, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nInvalid data. Select a file.", 7, 50, "Error Message")
					continue
				chosen_path = Path(tag)
				if chosen_path.is_dir():
					filepath = str(chosen_path) + '/'
					continue
				if chosen_path.is_file():
					path_extensions = ''.join(chosen_path.suffixes)
					if path_extensions in extensions_list:
						return tag
					else:
						self.create_message("\nInvalid data. File extension not allowed.", 7, 50, "Error Message")
				else:
					self.create_message("\nInvalid data. Select a file.", 7, 50, "Error Message")
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def select_directory(self, filepath: str, height: int, width: int, title: str) -> str:
		"""
		Method that creates a directory selection box.

		Parameters:
			filepath (str): Initial path.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.

		Returns:
			tag (str): Selected directory.
		"""
		while True:
			code, tag = self.python_dialog.dselect(filepath = filepath, height = height, width = width, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nInvalid data. Select a directory.", 7, 50, "Error Message")
					continue
				chosen_path = Path(tag)
				if chosen_path.is_dir():
					return tag
				else:
					self.create_message("\nInvalid data. The directory doesn't exist.", 8, 50, "Error Message")
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_radiolist(self, text: str, height: int, width: int, choices: tuple, title: str) -> str:
		"""
		Method that creates a radiolist.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			choices (tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings. No more than one entry should be set to True.
			title (str): Title to display in the box.

		Returns:
			tag (str): Chosen option.
		"""
		while True:
			code, tag = self.python_dialog.radiolist(text = text, height = height, width = width, list_height = len(choices), choices = choices, title = title)
			if code == self.python_dialog.OK:
				valid_tags = {c[0] for c in choices}
				if tag in valid_tags:
					return tag
				self.create_message("\nSelect at least one option.", 7, 50, "Error Message")
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_checklist(self, text: str, height: int, width: int, choices: tuple, title: str) -> tuple:
		"""
		Method that creates a checklist.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			choices (tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings. No more than one entry should be set to True.
			title (str): Title to display in the box.

		Returns:
			tag (tuple): Chosen options.
		"""
		while True:
			code, tag = self.python_dialog.checklist(text = text, height = height, width = width, list_height = len(choices), choices = choices, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nSelect at least one option.", 7, 50, "Error Message")
					continue
				valid_tags = {c[0] for c in choices}
				if all(t in valid_tags for t in tag):
					return tag 
				else:
					self.create_message("\nThe selected value(s) are invalid.", 7, 50, "Error Message")
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (str): Text entered.
		"""
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not tag.strip():
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				elif len(tag) > 100:
					self.create_message("\nInvalid data. Size exceeded (100 characters).", 7, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_integer_inputbox(self, text: str, height: int, width: int, init: str) -> int:
		"""
		Method that creates an inputbox for entering integers. 

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (int): Integer entered.
		"""
		utils = libPyUtils()
		int_regex = compile(r'^\d+$')

		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not utils.validate_data_regex(tag.strip(), int_regex):
					self.create_message("\nInvalid data. Required value (Integer number).", 7, 50, "Error Message")
				elif len(tag.strip()) > 10:
					self.create_message("\nInvalid data. Size exceeded (10 characters).", 7, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_port_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox for entering port numbers. 

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (str): Port entered.
		"""
		utils = libPyUtils()
		port_regex = compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:			
				if not utils.validate_data_regex(tag.strip(), port_regex):
					self.create_message("\nInvalid data. Required value (Port number).", 7, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_filename_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox for entering a file name. 

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (str): File name entered.
		"""
		utils = libPyUtils()
		file_name_regex = compile(r'^[^\\/?%*:|"<>]+$')

		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not utils.validate_data_regex(tag.strip(), file_name_regex):
					self.create_message("\nInvalid data. Required value (File name).", 7, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_url_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox for entering a URL. 

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (str): URL entered.
		"""
		url_regex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not tag.strip():
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
					continue
				if len(tag.strip()) > 50:
					self.create_message("\nInvalid data. Exceeded size (maximum 50 characters).", 8, 50, "Error Message")
					continue
				if url_regex.match(tag.strip()):
					return tag
				else:
					self.create_message("\nInvalid data. Required value (URL).", 8, 50, "Error Message")
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_passwordbox(self, text: str, height: int, width: int, init: str, insecure_mode: bool) -> str:
		"""
		Method that creates an inputbox of type password.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.
			insecure_mode (bool): Enable insecure mode or not (show '*' character on screen or not).

		Returns:
			tag (str): Password entered.
		"""
		while True:
			code, tag = self.python_dialog.passwordbox(text = text, height = height, width = width, init = init, insecure = insecure_mode)
			if code == self.python_dialog.OK:
				if not tag or not tag.strip():
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_time(self, text: str, height: int, width: int, hour: int, minute: int) -> list:
		"""
		Method that creates a timebox.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			hour (int): Default hour.
			minute (int): Default minute.

		Returns:
			tag (list): Selected time.
		"""
		code, tag = self.python_dialog.timebox(text = text, height = height, width = width, hour = hour, minute = minute, second = 0)
		if code == self.python_dialog.OK:
			if tag and len(tag) == 3:
				return tag
			else:
				self.create_message("\nInvalid time format.", 7, 50, "Error Message")
		elif code == self.python_dialog.CANCEL:
			raise KeyboardInterrupt("Exit")


	def create_yes_or_no(self, text: str, height: int, width: int, title: str) -> str:
		"""
		Method that creates a yes/no box.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.

		Returns:
			tag (str): Chosen option.
		"""
		tag = self.python_dialog.yesno(text = text, height = height, width = width, title = title)
		value = tag == "ok"
		return value


	def create_scrollbox(self, text: str, height: int, width: int, title: str) -> None:
		"""
		Method that creates a scrollbox.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
		"""
		code = self.python_dialog.scrollbox(text = text, height = height, width = width, title = title)
		if code == self.python_dialog.ESC:
			raise KeyboardInterrupt("Exit")
