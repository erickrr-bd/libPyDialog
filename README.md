# libPyDialog v2.2

Python library that extends the capabilities to create TUI (Text User Interface) type graphical interfaces in console environments.

It incorporates integrated validations to ensure the quality and consistency of the data entered by the user, facilitating the development of interactive, secure and modular applications.

## Features
- Based on [pythondialog](https://pythondialog.sourceforge.net/)
- Automatic validation of entries (numbers, emails, dates, IP addresses, URLs, etc.)
- Modular and easy to integrate into CLI scripts
- Compatible with Linux systems and POSIX environments
- Ideal for administrative tools, installers and interactive wizards

## Requirements
- Red Hat 8 or Rocky Linux 8
- Dialog
- Python 3.12
- Python Libraries
  - pythondialog
  - [libPyUtils v2.2](https://github.com/erickrr-bd/libPyUtils)

## Dialog Installation

It's required to have Dialog installed on the system. To install it on Rocky Linux:

```
sudo dnf -y install dialog
```

## Installation

Copy the "libPyDialog" folder to the following path:

`/usr/local/lib/python3.12/site-packages`

**NOTE:** The path may change depending on the version of Python.

## Documentation

See the project wiki for advanced examples, integration with Bash scripts, and theme customization.
