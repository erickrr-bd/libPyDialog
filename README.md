# libPyDialog

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Version](https://img.shields.io/badge/version-2.4.0-green)

Python library that enhances the use of [pythondialog](https://pythondialog.sourceforge.io/) to build **TUI-type interfaces on terminals**, with **input validation built in**.

Instead of calling `pythondialog` directly and validating every answer yourself, `libPyDialog` gives you ready-made dialogs (menus, forms, input boxes for integers, ports, file names, URLs and passwords, file selectors, and more) that **keep asking until the data is valid** or the user cancels.

## Features

- One method per kind of dialog, with a consistent signature: `text`, `height`, `width`, ... `title`.
- Built-in validation with an error message box and a retry loop: non-empty values, maximum length, integer ranges, ports, file names, URLs, CPE-like formats (through your own validator), and more.
- Returns clean values: text is stripped, integers are returned as `int`, yes/no as `bool`.
- Returned options are checked against the options that were offered (radiolist and checklist).
- Hidden input for secrets (`create_passwordbox`), with optional length limit and custom validator.
- Lists, menus and forms with more items than fit on screen **scroll** instead of making `dialog` fail.
- The `dialog` binary is located through **absolute paths only**, never through `PATH`.
- A dedicated `DialogCancelled` exception to tell "the user cancelled" apart from a real `Ctrl+C`.

## Requirements

| Requirement | Notes |
| --- | --- |
| Python | 3.10 or newer (tested with 3.13) |
| [pythondialog](https://pypi.org/project/pythondialog/) | Python wrapper (`import dialog`) |
| `dialog` binary | Installed in `/usr/bin`, `/usr/local/bin` or `/bin` (for example `apt install dialog` or `dnf install dialog`) |
| [libPyUtils](https://github.com/erickrr-bd/libPyUtils) | Used for regular-expression validation |

## Installation

```bash
git clone https://github.com/erickrr-bd/libPyDialog.git
pip install pythondialog
```

Copy `libPyDialog.py` into your project, or add the cloned folder to your `PYTHONPATH`. Make sure `libPyUtils` is importable as well.

## Quick start

```python
from libPyDialog import libPyDialog, DialogCancelled

dialog = libPyDialog("My Application v1.0")

try:
	option = dialog.create_menu("Select an option:", 11, 50, (("1", "Configuration"), ("2", "Exit")), "Main Menu")

	# Integer between 1 and 120. The box is shown again until the value is valid.
	days = dialog.create_integer_inputbox("Enter the range of days:", 8, 50, "1", min_value = 1, max_value = 120)

	# Hidden input with a custom validator.
	api_key = dialog.create_passwordbox("Enter the API Key:", 9, 60, True, title = "API Key",
		validator = lambda value: len(value) == 36, error_message = "The API Key must have 36 characters.")

	# One row per element, every value validated.
	hosts = dialog.create_form("Enter the hosts:", dialog.utils.generate_tuple_to_form(3, "Host"), 15, 50, "Hosts",
		validator = lambda value: value.isascii(), error_message = "Only ASCII characters.")

	if dialog.create_yes_or_no("\nSave the changes?", 7, 50, "Confirmation"):
		dialog.create_message("\nSaved.", 7, 50, "Notification Message")
except DialogCancelled:
	pass  # the user pressed Cancel or ESC
```

## Dialogs

All dialogs share the arguments `text`, `height` and `width`; the last positional argument is the `title` (or `init`, for input boxes).

### Selection and display

| Method | Returns | Description |
| --- | --- | --- |
| `create_menu(text, height, width, choices, title)` | `str` | Menu. Returns the tag of the chosen entry. |
| `create_radiolist(text, height, width, choices, title)` | `str` | One option out of several. The result is checked against `choices`. |
| `create_checklist(text, height, width, choices, title)` | `tuple` | One or more options. At least one must be selected, and all of them must be valid. |
| `create_yes_or_no(text, height, width, title)` | `bool` | `True` for "Yes", `False` otherwise (it never raises `DialogCancelled`). |
| `create_message(text, height, width, title)` | `None` | Message box. |
| `create_scrollbox(text, height, width, title)` | `None` | Scrollable text. Pressing ESC raises `DialogCancelled`. |

`choices` for radiolists and checklists are `(tag, description, status)` tuples; for menus, `(tag, description)` tuples.

### Text and numeric input

| Method | Returns | Validation |
| --- | --- | --- |
| `create_inputbox(text, height, width, init)` | `str` | Stripped, not empty, at most 100 characters. |
| `create_integer_inputbox(text, height, width, init, min_value = 0, max_value = None)` | `int` | Digits only, at most 10 characters, inside `min_value` / `max_value`. |
| `create_port_inputbox(text, height, width, init)` | `str` | ASCII digits, between 1 and 65535. |
| `create_filename_inputbox(text, height, width, init)` | `str` | No `\ / ? % * : \| " < >`, no control characters, not `.` or `..`, at most 255 characters. |
| `create_url_inputbox(text, height, width, init)` | `str` | `http(s)` URL, at most 50 characters. **URLs with credentials (`user:pass@host`) are rejected.** |
| `create_passwordbox(text, height, width, insecure_mode, title = "", max_len = 256, validator = None, error_message = ...)` | `str` | Stripped, not empty, at most `max_len`, plus your optional `validator`. |
| `create_time(text, height, width, hour, minute)` | `list` | Returns `[hour, minute, second]`. Pass `-1, -1` to start from the current time. |

`create_passwordbox(..., insecure_mode = True)` shows an asterisk for every character typed; with `False` nothing is displayed.

### Forms

| Method | Returns | Description |
| --- | --- | --- |
| `create_form(text, elements, height, width, title, validator = None, error_message = ...)` | `list` | Form with several fields. Every value is stripped, must not be empty, at most 100 characters, and must pass `validator` if given. |
| `create_url_form(text, elements, height, width, title)` | `list` | Form where every value must be `http(s)://host:port` (the port is mandatory; no path, query or fragment). |

A `validator` is any function that receives one value and returns `True` when it is acceptable. When it returns `False`, `error_message` is shown and the form is displayed again.

### Files and directories

| Method | Returns | Description |
| --- | --- | --- |
| `select_file(filepath, height, width, title, extensions_list)` | `str` | File selector. Only files with an allowed extension are accepted. Returns the resolved path. |
| `select_directory(filepath, height, width, title)` | `str` | Directory selector. Returns the resolved path of an existing directory. |

`create_file` remains available as an alias of `select_file` for backwards compatibility.

## Cancelling

Pressing **Cancel** or **ESC** in any input dialog raises `DialogCancelled`.

`DialogCancelled` is a subclass of `KeyboardInterrupt`, so:

- existing `except KeyboardInterrupt:` blocks keep working, and
- you can catch only user cancellations and let a real `Ctrl+C` reach your main program:

```python
try:
	while True:
		option = dialog.create_menu(...)
except DialogCancelled:
	pass            # Cancel / ESC in the menu
except KeyboardInterrupt:
	raise SystemExit  # a real Ctrl+C
```

Note that `DialogCancelled` does **not** inherit from `Exception`: a `except Exception:` block will not swallow it.

## Security notes

- The `dialog` binary is searched only in `/usr/bin/dialog`, `/usr/local/bin/dialog` and `/bin/dialog`. It is never resolved through `PATH`, so a malicious entry in `PATH` cannot replace it. `FileNotFoundError` is raised if it is not installed.
- Every value entered by the user is validated before it is returned. Validate again when you use it in a sensitive context (file paths, shell commands, URLs): these checks are a first line of defense, not a replacement.
- Use `create_passwordbox` for secrets, never `create_inputbox`: the input box shows what is typed and can pre-fill a value.
- Integer inputs accept at most 10 digits, and list-like dialogs scroll instead of growing without limit. Always pass `max_value` when the number is used to size something (for example, how many form rows to draw).

## Migrating from 2.3.1

- **`DialogCancelled`** replaces `raise KeyboardInterrupt("Exit")` in every dialog. It is a `KeyboardInterrupt` subclass, so existing handlers still work.
- **`create_passwordbox`** gained `title`, `max_len`, `validator` and `error_message`, and now returns the stripped value. Existing calls keep working.
- **`create_integer_inputbox`** gained `min_value` and `max_value`.
- **`create_form`** now strips every value and accepts `validator` and `error_message`. `create_url_form` is now a thin wrapper around it.
- **`create_url_inputbox`** now rejects URLs that contain credentials.
- **`create_inputbox`** now returns the stripped text.
- **`create_file`** was renamed `select_file`, to avoid confusion with methods that create files. The old name still works.
- **Scrolling:** menus, radiolists, checklists and forms limit the visible rows to what fits in the box.
- `from re import compile` was replaced by `import re`, so the built-in `compile()` is no longer shadowed.

## Author

**Erick Roberto Rodriguez Rodriguez**
[erodriguez@tekium.mx](mailto:erodriguez@tekium.mx) · [erickrr.tbd93@gmail.com](mailto:erickrr.tbd93@gmail.com) · [GitHub](https://github.com/erickrr-bd/libPyDialog)

