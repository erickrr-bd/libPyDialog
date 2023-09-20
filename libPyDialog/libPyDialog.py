from os import path
from dialog import Dialog
from libPyUtils import libPyUtils
from re import compile as re_compile

class libPyDialog:

	def __init__(self, background_title):
		"""
		Class constructor.

		:arg background_title (string): Title to display in the background of the box.
		"""
		self.__utils = libPyUtils()
		self.__diag = Dialog(dialog = "dialog")
		self.integer_regex = re_compile(r'^\d+$')
		self.__diag.set_background_title(background_title)
		self.file_folder_name_regex = re_compile(r'^[^\\/?%*:|"<>]+$')
		self.port_number_regex = re_compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		self.ip_address_regex = re_compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')


	def createMenuDialog(self, text, height, width, choices, title):
		"""
		Method that creates a menu.

		Returns a string with the number of the chosen option.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg choices (tuple): Tuple with the menu options.	
		:arg title (string): Title to display in the box.
		"""
		code_menu, tag_menu = self.__diag.menu(text = text, height = height, width = width, menu_height = len(choices), choices = choices, title = title)
		if code_menu == self.__diag.OK:
			return tag_menu
		elif code_menu == self.__diag.CANCEL:
			raise KeyboardInterrupt("Exit")


	def createMessageDialog(self, text, height, width, title):
		"""
		Method that displays a message.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg title (string): Title to display in the box.
		"""
		self.__diag.msgbox(text = text, height = height, width = width, title = title)


	def createRadioListDialog(self, text, height, width, choices, title):
		"""
		Method that creates a radiolist.

		Returns a string with the chosen option.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg choices (tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings. No more than one entry should be set to True.
		:arg title (string): Title to display in the box.
		"""
		while True:
			code_radiolist, tag_radiolist = self.__diag.radiolist(text = text, height = height ,width = width, list_height = len(choices), choices = choices, title = title)
			if code_radiolist == self.__diag.OK:
				if not tag_radiolist:
					self.createMessageDialog("\nSelect at least one option.", 7, 50, "Error Message")
				else:
					return tag_radiolist
			elif code_radiolist == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")


	def createCheckListDialog(self, text, height, width, choices, title):
		"""
		Method that creates a checklist.

		Returns a tuple with the chosen options.
		
		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg choices (tuple): An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings.
		:arg title (string): Title to display in the box.
		"""
		while True:
			code_checklist, tag_checklist = self.__diag.checklist(text = text, height = height, width = width, list_height = len(choices), choices = choices, title = title)
			if code_checklist == self.__diag.OK:
				if not tag_checklist:
					self.createMessageDialog("\nSelect at least one option.", 7, 50, "Error Message")
				else:
					return tag_checklist
			elif code_checklist == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")

	
	def createInputBoxDialog(self, text, height, width, init):
		"""
		Method that creates an inputbox.

		Returns the string with the entered data.
	
		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg init (string): Default input string.
		"""
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if not tag_inputbox:
					self.createMessageDialog("\nInvalid data entered. Required value (not empty).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")


	def createPasswordBoxDialog(self, text, height, width, init, insecure):
		"""
		Method that creates an inputbox of type password.

		Returns a string with the password entered.
	
		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg init (string): Default input string.
		:arg insecure (boolean): If the value is True, the entered password is displayed with the character *. Otherwise the password does not appear.
		"""
		while True:
			code_passwordbox, tag_passwordbox = self.__diag.passwordbox(text = text, height = height, width = width, init = init, insecure = insecure)
			if code_passwordbox == self.__diag.OK:
				if not tag_passwordbox:
					self.createMessageDialog("\nInvalid data entered. Required value (not empty).", 8, 50, "Error Message")
				else:
					return tag_passwordbox
			elif code_passwordbox == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")

	
	def createInputBoxToNumberDialog(self, text, height, width, init):
		"""
		Method that creates an inputbox for entering integers.

		Returns a string with the entered number.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg init (string): Default input string.
		"""
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataRegex(self.integer_regex, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required value (integer number).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")

	
	def createInputBoxToPortDialog(self, text, height, width, init):
		"""
		Method that creates an inputbox for entering port numbers.
		
		Returns a string with the entered port number.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg init (string): Default input string.
		"""
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataRegex(self.port_number_regex, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required value (0 - 65535).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")


	def createFolderOrFileNameDialog(self, text, height, width, init):
		"""
		Method that creates an inputbox to enter the name of a file or folder.
		
		Returns a string with the name of the file or folder entered.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg init (string): Default input string.
		"""
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataRegex(self.file_folder_name_regex, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required data (File or folder name).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")


	def createTimeDialog(self, text, height, width, hour, minute):
		"""
		Method that creates a timebox.
		
		Returns a list with the chosen time.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg hour (integer): Inititial hour selected.
		:arg minute (integer): inititial minute selected.
		"""
		code_timebox, tag_timebox = self.__diag.timebox(text = text, height = height, width = width, hour = hour, minute = minute, second = 00)
		if code_timebox == self.__diag.OK:
			return tag_timebox
		elif code_timebox == self.__diag.CANCEL:
			raise KeyboardInterrupt("Exit")


	def createFileDialog(self, filepath, height, width, title, allowed_file_extension):
		"""
		Method that creates a file selection box.
		
		Returns a string with the chosen path.

		:arg filepath (string): Initial path.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg title (string): Title to display in the box.
		:arg allowed_file_extension (string): Allowed file extension.
		"""
		while True:
			code_fselect, tag_fselect = self.__diag.fselect(filepath = filepath, height = height, width = width, title = title)
			if code_fselect == self.__diag.OK:
				if not tag_fselect:
					self.createMessageDialog("\nSelect a file. Required value: " + allowed_file_extension + " file.", 7, 50, "Error Message")
				elif not path.isfile(tag_fselect):
					self.createMessageDialog("\nFile doesn't exist. Select a file.", 7, 50, "Error Message")
				else:
					file_extension = path.splitext(tag_fselect)[1]
					if not file_extension == allowed_file_extension:
						self.createMessageDialog("\nSelect an allowed file. Required value: " + allowed_file_extension + " file.", 7, 50, "Error Message")
					else:
						return tag_fselect
			elif code_fselect == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")


	def createFolderDialog(self, filepath, height, width, title):
		"""
		Method that creates a folder selection box.
		
		Returns a string with the chosen path.

		:arg filepath (string): Initial path.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg title (string): Title to display in the box.
		"""
		while True:
			code_dselect, tag_dselect = self.__diag.dselect(filepath = filepath, height = height, width = width, title = title)
			if code_dselect == self.__diag.OK:
				if tag_dselect == "":
					self.createMessageDialog("\nSelect a folder. Required value (not empty).", 7, 50, "Error Message")
				else:
					return tag_dselect
			elif code_dselect == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")

	
	def createFormDialog(self, text, elements, height, width, title, is_data_validated, **kwargs):
		"""
		Method that creates a form.
		
		Returns a list with the entered data.

		:arg text (string): Text to display in the box.
		:arg elements (tuple): Sequence describing the labels and fields.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg title (string): Title to display in the box.
		:arg is_data_validated (boolean): If the data entered will be validated or not.

		Keyword Args:
        	:arg option_validate (integer): Data type to validate. Option one is to validate that the data entered are IP addresses.
		"""
		while True:
			code_form, tag_form = self.__diag.form(text = text, elements = elements, height = height, width = width, form_height = len(elements), title = title)
			if code_form == self.__diag.OK:
				if "" in tag_form:
					self.createMessageDialog("\nThere should be no empty fields in the form.", 7, 50, "Error Message")
				else:
					if is_data_validated:
						if "option_validate" in kwargs:
							if kwargs["option_validate"] == 1:
								cont = 0
								for tag in tag_form:
									if self.__utils.validateDataRegex(self.ip_address_regex, tag):
										cont += 1
								if cont == len(elements):
									return tag_form
								else:
									self.createMessageDialog("\nThe data must be IP addresses.", 7, 50, "Error Message")
					else:
						return tag_form
			elif code_form == self.__diag.CANCEL:
				raise KeyboardInterrupt("Exit")


	def createYesOrNoDialog(self, text, height, width, title):
		"""
		Method that creates a yes/no box.
		
		Returns a string with the chosen option.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg title (string): Title to display in the box.
		"""
		tag_yes_no = self.__diag.yesno(text = text, height = height, width = width, title = title)
		return tag_yes_no


	def createScrollBoxDialog(self, text, height, width, title):
		"""
		Method that creates a scrollbox.

		:arg text (string): Text to display in the box.
		:arg height (integer): Height of the box.
		:arg width (integer): Width of the box.
		:arg title (string): Title to display in the box.
		"""
		code_scrollbox = self.__diag.scrollbox(text = text, height = height, width = width, title = title)