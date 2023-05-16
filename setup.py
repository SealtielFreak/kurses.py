from setuptools import setup

MODULE_TITLE = "pyrogue"
MODULE_VERSION = "2.0"
MODULE_DESCRIPTION = """
This module provides a cross-platform solution for simulating the functionality of the conio and curses libraries. It allows users to easily create text-based user interfaces with advanced features such as color and cursor control. The module is designed to be easy to use and provides a high level of compatibility with existing code that uses conio or curses.
"""

setup(
    name=MODULE_TITLE,
    version=MODULE_VERSION,
    description=MODULE_DESCRIPTION,
    author='Sealtiel Valderrama',
    author_email="sealtielfreak@yandex.com",
    packages=["pyrogue"],
    install_requires=[""],
)