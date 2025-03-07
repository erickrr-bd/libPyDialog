"""
Author: Erick Roberto Rodriguez Rodriguez
Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com
GitHub: https://github.com/erickrr-bd/libPyDialog
libPyDialog v2.2 - March 2025
"""
from re import compile
from pathlib import Path
from dialog import Dialog
from libPyUtils import libPyUtils
from dataclasses import dataclass

@dataclass
class libPyDialog:
	"""
	Easy creation of graphical interfaces using PythonDialog. 
	"""
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


	def create_form(self, text: str, elements: tuple, height: int, width: int, title: str, is_validate: bool, **kwargs) -> list:
		"""
		Method that creates a form.

		Parameters:
			text (str): Text to display in the box.
			elements (tuple): Sequence describing the labels and fields.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
			is_validate (bool): Option that indicates whether the entered data is validated or not.

		Keyword Args:
			validation_type (int): Validation type (Option one - IP address, hostname, domain name)

		Returns:
			tag (list): List with the data entered in the form.
		"""
		utils = libPyUtils()
		while True:
			code, tag = self.python_dialog.form(text = text, elements = elements, height = height, width = width, form_height = len(elements), title = title)
			if code == self.python_dialog.OK:
				if "" in tag:
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				else:
					if is_validate:
						if "validation_type" in kwargs:
							match kwargs["validation_type"]:
								case 1:
									cont = 0
									domain_name_regex = compile(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
									ip_regex = compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
									for data in tag:
										if utils.validate_data_regex(data, ip_regex) or utils.validate_data_regex(data, domain_name_regex):
											cont += 1
									if cont == len(elements):
										return tag
									else:
										self.create_message("\nInvalid data. Required value (IP address, hostname or domain name).", 8, 50, "Error Message")
					else:
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
					self.create_message("Invalid data. Select a file.", 7, 50, "Error Message")
				else:
					path_extensions = ''.join(tag.suffixes)
					if tag.is_file() and path_extensions in extensions_list:
						return tag
					else:
						self.create_message("\nInvalida data. File extension not allowed.", 7, 50, "Error Message")
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
				if not tag:
					self.create_message("\nSelect at least one option.", 7, 50, "Error Message")
				else:
					return tag
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
				else:
					return tag
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
			tag (str): Data entered.
		"""
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_integer_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox for entering integers. 

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (str): Integer entered.
		"""
		utils = libPyUtils()
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				number_regex = compile(r'^\d+$')
				if not utils.validate_data_regex(tag, number_regex):
					self.create_message("\nInvalid data. Required value (Integer number).", 7, 50, "Error Message")
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
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				port_regex = compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
				if not utils.validate_data_regex(tag, port_regex):
					self.create_message("\nInvalid data. Required value (Port number).", 7, 50, "Error Message")
				else:
					return tag
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
				if not tag:
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				else:
					return tag
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
		return tag


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