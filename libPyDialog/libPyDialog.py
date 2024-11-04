"""
Author: Erick Roberto Rodriguez Rodriguez
Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com
GitHub: https://github.com/erickrr-bd/libPyDialog
libPyDialog v2.1 - October 2024
"""
from os import path
from re import compile
from dialog import Dialog
from libPyUtils import libPyUtils

class libPyDialog:

	def __init__(self, background_title):
		"""
		Class constructor.

		:arg background_title (String): Text displayed in the background.
		"""
		self.utils = libPyUtils()
		self.python_dialog = Dialog(dialog = "dialog")
		self.python_dialog.set_background_title(background_title)


	def create_message(self, text, height, width, title):
		"""
		Method that displays a message.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg title (String): Title to display in the box.
		"""
		self.python_dialog.msgbox(text = text, height = height, width = width, title = title)


	def create_menu(self, text, height, width, choices, title):
		"""
		Method that creates a menu.

		Returns a string with the chosen option.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg choices (Tuple): Tuple with the menu options.	
		:arg title (String): Title to display in the box.
		"""
		code, tag = self.python_dialog.menu(text = text, height = height, width = width, menu_height = len(choices), choices = choices, title = title)
		if code == self.python_dialog.OK:
			return tag
		elif code == self.python_dialog.CANCEL:
			raise KeyboardInterrupt("Exit")


	def create_form(self, text, elements, height, width, title, is_validate, **kwargs):
		"""
		Method that creates a form.
		
		Returns a list.

		:arg text (String): Text to display in the box.
		:arg elements (Tuple): Sequence describing the labels and fields.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg title (String): Title to display in the box.
		:arg is_validate (Boolean): Option to validate the data entered.

		Keyword Args:
        	:arg validation_type (Integer): Validation type (Option one - IP address, hostname, domain name)
		"""
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
										if self.utils.validate_data_regex(data, ip_regex) or self.utils.validate_data_regex(data, domain_name_regex):
											cont += 1
									if cont == len(elements):
										return tag
									else:
										self.create_message("\nInvalid data. Required value (IP address, hostname or domain name).", 8, 50, "Error Message")
					else:
						return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_file(self, filepath, height, width, title, file_ext):
		"""
		Method that creates a file selection box.
		
		Returns a string with the selected path.

		:arg filepath (String): Initial path.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg title (String): Title to display in the box.
		:arg file_ext (String): Extension allowed.
		"""
		while True:
			code, tag = self.python_dialog.fselect(filepath = filepath, height = height, width = width, title = title)
			if code == self.python_dialog.OK:
				if not tag:
					self.create_message("\nInvalida data. Required value: " + file_ext + " file.", 7, 50, "Error Message")
				elif not path.isfile(tag):
					self.create_message("\nFile doesn't exist. Required value: " + file_ext + " file.", 7, 50, "Error Message")
				else:
					extension = path.splitext(tag)[1]
					if not file_ext == extension:
						self.create_message("\nInvalida data. Required value: " + file_ext + " file.", 7, 50, "Error Message")
					else:
						return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_radiolist(self, text, height, width, choices, title):
		"""
		Method that creates a radiolist.

		Returns a string with the chosen option.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg choices (Tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings. No more than one entry should be set to True.
		:arg title (String): Title to display in the box.
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


	def create_checklist(self, text, height, width, choices, title):
		"""
		Method that creates a checklist.

		Returns a tuple with the chosen options.
	
		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg choices (Tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings.
		:arg title (String): Title to display in the box.
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


	def create_inputbox(self, text, height, width, init):
		"""
		Method that creates an inputbox.

		Returns the string with the entered data.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg init (String): Default input string.
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


	def create_integer_inputbox(self, text, height, width, init):
		"""
		Method that creates an inputbox for entering integers. 

		Returns a string with the entered number.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg init (String): Default input string.
		"""
		number_regex = compile(r'^\d+$')
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not self.utils.validate_data_regex(tag, number_regex):
					self.create_message("\nInvalid data. Required value (Integer number).", 7, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_port_inputbox(self, text, height, width, init):
		"""
		Method that creates an inputbox for entering port numbers. 

		Returns a string with the entered port.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg init (String): Default input string.
		"""
		port_regex = compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code, tag = self.python_dialog.inputbox(text = text, height = height, width = width, init = init)
			if code == self.python_dialog.OK:
				if not self.utils.validate_data_regex(tag, port_regex):
					self.create_message("\nInvalid data. Required value (Port number).", 7, 50, "Error Message")
				else:
					return tag
			elif code == self.python_dialog.CANCEL:
				raise KeyboardInterrupt("Exit")


	def create_passwordbox(self, text, height, width, init, insecure_mode):
		"""
		Method that creates an inputbox of type password.

		Returns a string with the password entered.
	
		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg init (String): Default input string.
		:arg insecure_mode (Boolean): Enable insecure mode or not (show '*' character on screen or not).
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


	def create_yes_or_no(self, text, height, width, title):
		"""
		Method that creates a yes/no box.
		
		Returns a string with the chosen option.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg title (String): Title to display in the box.
		"""
		tag = self.python_dialog.yesno(text = text, height = height, width = width, title = title)
		return tag


	def create_scrollbox(self, text, height, width, title):
		"""
		Method that creates a scrollbox.

		:arg text (String): Text to display in the box.
		:arg height (Integer): Height of the box.
		:arg width (Integer): Width of the box.
		:arg title (String): Title to display in the box.
		"""
		code = self.python_dialog.scrollbox(text = text, height = height, width = width, title = title)