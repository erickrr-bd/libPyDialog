"""
Author: Erick Roberto Rodriguez Rodriguez
Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com
GitHub: https://github.com/erickrr-bd/libPyDialog
libPyDialog v2.4.0 - November 2026
Python library that enhances the use of pythondialog to build TUI-type graphical interfaces on terminals.
"""
import re
from pathlib import Path
from dialog import Dialog
from urllib.parse import urlsplit
from libPyUtils import libPyUtils

# Absolute paths where the "dialog" binary is trusted (avoids resolving it through PATH).
DIALOG_PATHS = ("/usr/bin/dialog", "/usr/local/bin/dialog", "/bin/dialog")

# Regular expressions compiled once at import time.
INT_REGEX = re.compile(r'^[0-9]+$')
FILENAME_REGEX = re.compile(r'^[^\\/?%*:|"<>]+$')
URL_REGEX = re.compile(r"^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$")
HOSTNAME_REGEX = re.compile(r'^[A-Za-z0-9.-]+$')


class DialogCancelled(KeyboardInterrupt):
	"""
	Raised when the user presses Cancel or ESC in a dialog.
	It inherits from KeyboardInterrupt so existing "except KeyboardInterrupt" blocks keep working,
	but it can be told apart from a real Ctrl+C.
	"""


def _find_dialog() -> str:
	"""
	Function that locates the dialog binary using absolute paths only.

	Returns:
		path (str): Absolute path of the dialog binary.
	"""
	for path in DIALOG_PATHS:
		if Path(path).is_file():
			return path
	raise FileNotFoundError("The 'dialog' binary was not found in: " + ", ".join(DIALOG_PATHS))


def _is_valid_url_port(value: str) -> bool:
	"""
	Function that validates a value in URL:PORT format (http(s)://host:port).

	Parameters:
		value (str): Value to validate.

	Returns:
		is_valid (bool): True if the value is valid.
	"""
	if value != value.strip() or any(char.isspace() for char in value):
		return False
	try:
		parts = urlsplit(value)
		port = parts.port
	except ValueError:
		return False
	return (parts.scheme in ("http", "https")
		and bool(parts.hostname)
		and HOSTNAME_REGEX.fullmatch(parts.hostname) is not None
		and port is not None
		and 0 < port <= 65535
		and parts.path in ("", "/")
		and not parts.query
		and not parts.fragment)


class libPyDialog:

	python_dialog: Dialog

	def __init__(self, backtitle: str):
		"""
		Class constructor.

		Parameters:
			backtitle (str): Text displayed in the background.
		"""
		self.python_dialog = Dialog(dialog = _find_dialog())
		self.python_dialog.set_background_title(backtitle)
		self.utils = libPyUtils()


	@staticmethod
	def _list_height(total_items: int, box_height: int) -> int:
		"""
		Method that calculates how many rows of a list/menu/form fit in a box (the rest scrolls).

		Parameters:
			total_items (int): Total elements.
			box_height (int): Height of the box.

		Returns:
			height (int): Rows to show.
		"""
		return max(1, min(total_items, box_height - 7))


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


	def _validate_form_values(self, values: list, extra_check = None, error_message: str = "Invalid data.") -> bool:
		"""
		Method that validates the values entered in a form.

		Parameters:
			values (list): Values entered in the form.
			extra_check (callable): Optional additional validation (receives a value, returns bool).
			error_message (str): Message displayed when extra_check fails.

		Returns:
			is_valid (bool): True if all the values are valid.
		"""
		for value in values:
			if not value.strip():
				self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				return False
			if len(value) > 100:
				self.create_message("\nInvalid data. Size exceeded (100 characters).", 8, 50, "Error Message")
				return False
			if extra_check is not None and not extra_check(value):
				self.create_message(f"\n{error_message}\n\nValue: {value[:40]}", 10, 55, "Error Message")
				return False
		return True


	def create_menu(self, text: str, height: int, width: int, choices: tuple, title: str) -> str:
		"""
		Method that creates a menu.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			choices (tuple): Tuple with the menu options.
			title (str): Title to display in the box.

		Returns:
			tag (str): Option chosen from the menu.
		"""
		code, tag = self.python_dialog.menu(text = text, height = height, width = width, menu_height = self._list_height(len(choices), height), choices = choices, title = title)
		if code == self.python_dialog.OK:
			return tag
		raise DialogCancelled("Exit")


	def create_form(self, text: str, elements: tuple, height: int, width: int, title: str, validator = None, error_message: str = "Invalid data.") -> list:
		"""
		Method that creates a form. The returned values are stripped.

		Parameters:
			text (str): Text to display in the box.
			elements (tuple): Sequence describing the labels and fields.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
			validator (callable): Optional validation applied to every value (receives a value, returns bool).
			error_message (str): Message displayed when the validator fails.

		Returns:
			tag (list): List with the data entered in the form.
		"""
		while True:
			code, tag = self.python_dialog.form(text = text, elements = elements, height = height, width = width, form_height = self._list_height(len(elements), height), title = title)
			if code == self.python_dialog.OK:
				values = [value.strip() for value in tag]
				if self._validate_form_values(values, validator, error_message):
					return values
			else:
				raise DialogCancelled("Exit")


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
		return self.create_form(text, elements, height, width, title, validator = _is_valid_url_port, error_message = "Invalid data. Required value (URL).")


	def select_file(self, filepath: str, height: int, width: int, title: str, extensions_list: list) -> str:
		"""
		Method that creates a file selection box.

		Parameters:
			filepath (str): Initial path.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.
			extensions_list (list): List of allowed extensions.

		Returns:
			tag (str): Selected file (resolved path).
		"""
		allowed_extensions = tuple(extension.lower() for extension in extensions_list)

		while True:
			code, tag = self.python_dialog.fselect(filepath = filepath, height = height, width = width, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nInvalid data. Select a file.", 7, 50, "Error Message")
					continue
				chosen_path = Path(tag).resolve()
				if chosen_path.is_dir():
					filepath = str(chosen_path) + '/'
					continue
				if chosen_path.is_file():
					if chosen_path.name.lower().endswith(allowed_extensions):
						return str(chosen_path)
					self.create_message("\nInvalid data. File extension not allowed.", 7, 50, "Error Message")
				else:
					self.create_message("\nInvalid data. Select a file.", 7, 50, "Error Message")
			else:
				raise DialogCancelled("Exit")


	# Alias kept for backwards compatibility. Use select_file().
	create_file = select_file


	def select_directory(self, filepath: str, height: int, width: int, title: str) -> str:
		"""
		Method that creates a directory selection box.

		Parameters:
			filepath (str): Initial path.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.

		Returns:
			tag (str): Selected directory (resolved path).
		"""
		while True:
			code, tag = self.python_dialog.dselect(filepath = filepath, height = height, width = width, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nInvalid data. Select a directory.", 7, 50, "Error Message")
					continue
				chosen_path = Path(tag).resolve()
				if chosen_path.is_dir():
					return str(chosen_path)
				self.create_message("\nInvalid data. The directory doesn't exist.", 8, 50, "Error Message")
			else:
				raise DialogCancelled("Exit")


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
		valid_tags = {choice[0] for choice in choices}

		while True:
			code, tag = self.python_dialog.radiolist(text = text, height = height, width = width, list_height = self._list_height(len(choices), height), choices = choices, title = title)
			if code == self.python_dialog.OK:
				if tag in valid_tags:
					return tag
				self.create_message("\nSelect at least one option.", 7, 50, "Error Message")
			else:
				raise DialogCancelled("Exit")


	def create_checklist(self, text: str, height: int, width: int, choices: tuple, title: str) -> tuple:
		"""
		Method that creates a checklist.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			choices (tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings.
			title (str): Title to display in the box.

		Returns:
			tag (tuple): Chosen options.
		"""
		valid_tags = {choice[0] for choice in choices}

		while True:
			code, tag = self.python_dialog.checklist(text = text, height = height, width = width, list_height = self._list_height(len(choices), height), choices = choices, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nSelect at least one option.", 7, 50, "Error Message")
					continue
				if all(value in valid_tags for value in tag):
					return tag
				self.create_message("\nThe selected value(s) are invalid.", 7, 50, "Error Message")
			else:
				raise DialogCancelled("Exit")


	def create_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox. The returned value is stripped.

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
				value = tag.strip()
				if not value:
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				elif len(value) > 100:
					self.create_message("\nInvalid data. Size exceeded (100 characters).", 7, 50, "Error Message")
				else:
					return value
			else:
				raise DialogCancelled("Exit")


	def create_integer_inputbox(self, text: str, height: int, width: int, init: str, min_value: int = 0, max_value: int = None) -> int:
		"""
		Method that creates an inputbox for entering integers.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.
			min_value (int): Minimum accepted value.
			max_value (int): Maximum accepted value (no limit if None).

		Returns:
			tag (int): Integer entered.
		"""
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				value = tag.strip()
				if not self.utils.validate_data_regex(value, INT_REGEX):
					self.create_message("\nInvalid data. Required value (Integer number).", 7, 50, "Error Message")
				elif len(value) > 10:
					self.create_message("\nInvalid data. Size exceeded (10 characters).", 7, 50, "Error Message")
				else:
					number = int(value)
					if number < min_value or (max_value is not None and number > max_value):
						limit = f"{min_value} to {max_value}" if max_value is not None else f"{min_value} or more"
						self.create_message(f"\nInvalid data. Allowed range: {limit}.", 7, 50, "Error Message")
					else:
						return number
			else:
				raise DialogCancelled("Exit")


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
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				value = tag.strip()
				if not (value.isascii() and value.isdigit() and 1 <= int(value) <= 65535):
					self.create_message("\nInvalid data. Required value (Port number).", 7, 50, "Error Message")
				else:
					return value
			else:
				raise DialogCancelled("Exit")


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
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				value = tag.strip()
				if (not self.utils.validate_data_regex(value, FILENAME_REGEX)
						or value in (".", "..")
						or len(value) > 255
						or any(ord(char) < 32 for char in value)):
					self.create_message("\nInvalid data. Required value (File name).", 7, 50, "Error Message")
				else:
					return value
			else:
				raise DialogCancelled("Exit")


	def create_url_inputbox(self, text: str, height: int, width: int, init: str) -> str:
		"""
		Method that creates an inputbox for entering a URL (credentials inside the URL are rejected).

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			init (str): Default input string.

		Returns:
			tag (str): URL entered.
		"""
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				value = tag.strip()
				if not value:
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
					continue
				if len(value) > 50:
					self.create_message("\nInvalid data. Exceeded size (maximum 50 characters).", 8, 50, "Error Message")
					continue
				try:
					has_userinfo = "@" in urlsplit(value).netloc
				except ValueError:
					has_userinfo = True
				if URL_REGEX.fullmatch(value) and not has_userinfo:
					return value
				self.create_message("\nInvalid data. Required value (URL).", 8, 50, "Error Message")
			else:
				raise DialogCancelled("Exit")


	def create_passwordbox(self, text: str, height: int, width: int, insecure_mode: bool, title: str = "", max_len: int = 256, validator = None, error_message: str = "Invalid data.") -> str:
		"""
		Method that creates an inputbox of type password. The returned value is stripped.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			insecure_mode (bool): Enable insecure mode or not (show '*' character on screen or not).
			title (str): Title to display in the box.
			max_len (int): Maximum length accepted.
			validator (callable): Optional validation (receives the stripped value, returns bool).
			error_message (str): Message displayed when the validator fails.

		Returns:
			tag (str): Password entered.
		"""
		options = {"insecure": insecure_mode}
		if title:
			options["title"] = title
		while True:
			code, tag = self.python_dialog.passwordbox(text = text, height = height, width = width, **options)
			if code == self.python_dialog.OK:
				value = tag.strip() if tag else ""
				if not value:
					self.create_message("\nInvalid data. Required value (non-empty fields).", 8, 50, "Error Message")
				elif len(value) > max_len:
					self.create_message(f"\nInvalid data. Size exceeded ({max_len} characters).", 8, 50, "Error Message")
				elif validator is not None and not validator(value):
					self.create_message(f"\n{error_message}", 9, 55, "Error Message")
				else:
					return value
			else:
				raise DialogCancelled("Exit")


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
		while True:
			code, tag = self.python_dialog.timebox(text = text, height = height, width = width, hour = hour, minute = minute, second = 0)
			if code == self.python_dialog.OK:
				if tag and len(tag) == 3:
					return tag
				self.create_message("\nInvalid time format.", 7, 50, "Error Message")
			else:
				raise DialogCancelled("Exit")


	def create_yes_or_no(self, text: str, height: int, width: int, title: str) -> bool:
		"""
		Method that creates a yes/no box.

		Parameters:
			text (str): Text to display in the box.
			height (int): Height of the box.
			width (int): Width of the box.
			title (str): Title to display in the box.

		Returns:
			value (bool): True if the user chose "Yes", False otherwise.
		"""
		code = self.python_dialog.yesno(text = text, height = height, width = width, title = title)
		return code == self.python_dialog.OK


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
			raise DialogCancelled("Exit")