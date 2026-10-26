from pathlib import Path
from setuptools import find_packages, setup

HERE = Path(__file__).parent

VERSION = '2.3.1'
PACKAGE_NAME = 'libPyDialog' 
AUTHOR = 'Erick Roberto Rodríguez Rodriguez'
AUTHOR_EMAIL = 'erickrr.tbd93@gmail.com, erodriguez@tekium.mx' 
URL = 'https://github.com/erickrr-bd/libPyDialog' 

LICENSE = 'GPLv3' 
DESCRIPTION = 'Python library that enhances the use of pythondialog to build TUI-type graphical interfaces on terminals.' 
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding = 'utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'pythondialog'
      ]

setup(
    name = PACKAGE_NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = LONG_DESC_TYPE,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    install_requires = INSTALL_REQUIRES,
    license = LICENSE,
    packages = find_packages(),
    include_package_data = True
)