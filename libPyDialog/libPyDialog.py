from pathlib import Path
from dialog import Dialog
from libPyUtils import libPyUtils
from re import compile as re_compile

class libPyDialog:
	"""
	Attribute that contains an object of the dialog module (pythondialog library).
	"""
	__diag = None

	"""
	Attribute that contains an object of the libPyUtils library.
	"""
	__utils = None

	"""
	Attribute that contains the reference to the method that will be called when the user chooses the cancel option in the interfaces.
	"""
	__action_to_cancel = None


	def __init__(self, background_title, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg background_title: Title to display in the background of the box.
		:action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__utils = libPyUtils()
		self.__diag = Dialog(dialog = "dialog")
		self.__diag.set_background_title(background_title)
		self.__action_to_cancel = action_to_cancel


	def createMenuDialog(self, text, height, width, choices, title):
		"""
		Method that creates a dialog of type Menu. 

		Return the tag string that corresponding to the item that the user chose. Returns zero if the cancel option is chosen.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg choices: Tuple with the menu options.	
		:arg title: Title to display in the box.
		"""
		code_menu, tag_menu = self.__diag.menu(text = text, height = height, width = width, menu_height = len(choices), choices = choices, title = title)
		if code_menu == self.__diag.OK:
			return tag_menu
		if code_menu == self.__diag.CANCEL:
			return 0


	def createMessageDialog(self, text, height, width, title):
		"""
		Method to create a dialog of type Message.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg title: Title to display in the box.
		"""
		self.__diag.msgbox(text = text, height = height, width = width, title = title)


	def createRadioListDialog(self, text, height, width, choices, title):
		"""
		Method that creates a dialog of type RadioList.

		Return the tag string that corresponding to the entry that was chosen by the user.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg choices: An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings. No more than one entry should be set to True.
		:arg title: Title to display in the box.
		"""
		while True:
			code_radiolist, tag_radiolist = self.__diag.radiolist(text = text, height = height ,width = width, list_height = len(choices), choices = choices, title = title)
			if code_radiolist == self.__diag.OK:
				if not tag_radiolist:
					self.createMessageDialog("\nSelect at least one option.", 7, 50, "Error Message")
				else:
					return tag_radiolist
			elif code_radiolist == self.__diag.CANCEL:
				self.__action_to_cancel()


	def createCheckListDialog(self, text, height, width, choices, title):
		"""
		Method that creates a dialog of type CheckList.

		Return a tuple of the form (code, [tag, ...]) whose first element is a Dialog exit code and second element lists all tags for the entries selected by the user.
		
		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg choices: An iterable of (tag, item, status) tuples where status specifies the initial selected/unselected state of each entry; can be True or False, 1 or 0, "on" or "off" (True, 1 and "on" meaning selected), or any case variation of these two strings.
		:arg title: Title to display in the box.
		"""
		while True:
			code_checklist, tag_checklist = self.__diag.checklist(text = text, height = height, width = width, list_height = len(choices), choices = choices, title = title)
			if code_checklist == self.__diag.OK:
				if not tag_checklist:
					self.createMessageDialog("\nSelect at least one option.", 7, 50, "Error Message")
				else:
					return tag_checklist
			elif code_checklist == self.__diag.CANCEL:
				self.__action_to_cancel()

	
	def createInputBoxDialog(self, text, height, width, init):
		"""
		Method that creates a dialog of type inputbox.

		Return the string entered by the user.
	
		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg init: Default input string.
		"""
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if not tag_inputbox:
					self.createMessageDialog("\nInvalid data entered. Required value (not empty).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				self.__action_to_cancel()


	def createPasswordBoxDialog(self, text, height, width, init, insecure):
		"""
		Method that creates a dialog of type Password.

		Return the password entered by the user.
	
		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg init: Default input string.
		:arg insecure: If the value is True, the entered password is displayed with the character *. Otherwise the password does not appear.
		"""
		while True:
			code_passwordbox, tag_passwordbox = self.__diag.passwordbox(text = text, height = height, width = width, init = init, insecure = insecure)
			if code_passwordbox == self.__diag.OK:
				if not tag_passwordbox:
					self.createMessageDialog("\nInvalid data entered. Required value (not empty).", 8, 50, "Error Message")
				else:
					return tag_passwordbox
			elif code_passwordbox == self.__diag.CANCEL:
				self.__action_to_cancel()

	
	def createInputBoxToNumberDialog(self, text, height, width, init):
		"""
		Method that creates a dialog of type inputbox for integer numbers.

		Return the string (Integer value) entered by the user.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg init: Default input string.
		"""
		regular_expresion_to_number = re_compile(r'^\d+$')
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataWithRegularExpression(regular_expresion_to_number, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required value (integer number).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				self.__action_to_cancel()

	
	def createInputBoxToDecimalDialog(self, text, height, width, init):
		"""
		Method that creates a dialog of type inputbox for decimal numbers.

		Return the string (Decimal value) entered by the user.

		text -- Text to display in the box.
		height -- Height of the box.
		width -- Width of the box.
		init -- Default input string.
		"""
		regular_expresion_to_decimal = re_compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataWithRegularExpression(regular_expresion_to_decimal, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required value (decimal or float).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				self.__action_to_cancel()


	def createInputBoxToIPDialog(self, text, height, width, init):
		"""
		Method that creates a dialog of type inputbox for IP addresses.

		Return the string (IP address) entered by the user.

		text -- Text to display in the box.
		height -- Height of the box.
		width -- Width of the box.
		init -- Default input string.
		"""
		regular_expresion_to_ip = re_compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataWithRegularExpression(regular_expresion_to_ip, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required value (IP address).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				self.__action_to_cancel()

	
	def createInputBoxToPortDialog(self, text, height, width, init):
		"""
		Method that creates a dialog of type inputbox for IP addresses.
		
		Return the string (Port) entered by the user.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg init: Default input string.
		"""
		regular_expresion_to_port = re_compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataWithRegularExpression(regular_expresion_to_port, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required value (0 - 65535).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				self.__action_to_cancel()


	def createFolderOrFileNameDialog(self, text, height, width, init):
		"""
		Method that creates a dialog of type inputbox for folder or file name.
		
		Return the string (Folder or file name) entered by the user.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg init: Default input string.
		"""
		regular_expresion_to_name_folder_or_file = re_compile(r'^[^\\/?%*:|"<>]+$')
		while True:
			code_inputbox, tag_inputbox = self.__diag.inputbox(text = text, height = height, width = width, init = init)
			if code_inputbox == self.__diag.OK:
				if(not self.__utils.validateDataWithRegularExpression(regular_expresion_to_name_folder_or_file, tag_inputbox)):
					self.createMessageDialog("\nInvalid data entered. Required data (File or directory name).", 8, 50, "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.__diag.CANCEL:
				self.__action_to_cancel()


	def createTimeDialog(self, text, height, width, hour, minute):
		"""
		Method that creates a time dialog box.
		
		Return a list of the form [hour, minute, second], where hour, minute and second are integers corresponding to the time chosen by the user.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg hour: Inititial hour selected.
		:arg minute: inititial minute selected.
		"""
		code_timebox, tag_timebox = self.__diag.timebox(text = text, height = height, width = width, hour = hour, minute = minute, second = 00)
		if code_timebox == self.__diag.OK:
			return tag_timebox
		elif code_timebox == self.__diag.CANCEL:
			self.__action_to_cancel()


	def createFileDialog(self, filepath, height, width, title, extension_file):
		"""
		Method that creates a file selection dialog box.
		
		Return the path chosen by the user (the last element of which may be a directory or a file).

		:arg filepath: Initial path.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg title: Title to display in the box.
		:arg extension_file: Allowed file extension.
		"""
		while True:
			code_fselect, tag_fselect = self.__diag.fselect(filepath = filepath, height = height, width = width, title = title)
			if code_fselect == self.__diag.OK:
				if not tag_fselect:
					self.createMessageDialog("\nSelect a file. Required value: " + extension_file + " file.", 7, 50, "Error Message")
				else:
					ext_file = Path(tag_fselect).suffix
					if not ext_file == extension_file:
						self.createMessageDialog("\nSelect a file. Required value: " + extension_file + " file.", 7, 50, "Error Message")
					else:
						return tag_fselect
			elif code_fselect == self.__diag.CANCEL:
				self.__action_to_cancel()

	
	def createFormDialog(self, text, elements, height, width, title):
		"""
		Method that creates a form consisting of labels and fields.
		
		Return a list that gives the contents of every editable field on exit, with the same order as in elements.

		:arg text: Text to display in the box.
		:arg elements: sequence describing the labels and fields.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg title: Title to display in the box.
		"""
		while True:
			code_form, tag_form = self.__diag.form(text = text, elements = elements, height = height, width = width, form_height = len(elements), title = title)
			if code_form == self.__diag.OK:
				if "" in tag_form:
					self.createMessageDialog("\nNo form field can be empty.", 7, 50, "Error Message")
				else:
					return tag_form
			elif code_form == self.__diag.CANCEL:
				self.__action_to_cancel()


	def createYesOrNoDialog(self, text, height, width, title):
		"""
		Method that creates a yes/no dialog box.
		
		Return a Dialog exit code.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg title: Title to display in the box.
		"""
		tag_yes_or_no = self.__diag.yesno(text = text, height = height, width = width, title = title)
		return tag_yes_or_no


	def createScrollBoxDialog(self, text, height, width, title):
		"""
		Method that creates a dialog that shows a string in a scrollable box, with no line wrapping.
		
		Return a Dialog exit code.

		:arg text: Text to display in the box.
		:arg height: Height of the box.
		:arg width: Width of the box.
		:arg title: Title to display in the box.
		"""
		code_scrollbox = self.__diag.scrollbox(text = text, height = height, width = width, title = title)