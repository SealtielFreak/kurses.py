# kurses.py
![Python - Version](https://img.shields.io/badge/python-%3E%3D3.8-brightgreen)
![PyPI - Version](https://img.shields.io/pypi/v/kurses-py?color=green&label=pip%20install%20kurses)
![Python - Implementation](https://img.shields.io/pypi/implementation/kurses-py)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/kurses-py)

This module uses SDL2 (or Pygame) to emulate the functions of the [conio](https://en.wikipedia.org/wiki/Conio.h) and [curses](https://en.wikipedia.org/wiki/Curses_(programming_library)) libraries, which are used to create text-based user interfaces. You can control the color and cursor of the text, as well as the position and size of the window, the bit depth, typography and text styles (underline, bold, italic and strikethrough).

It is designed to offer a cross-platform solution for creating text-based applications, independent of the system where they run.

## How to install it?
You can install from pip:

```
pip install kurses-py
```

Or from GitHub repository:

```
pip install git+https://github.com/SealtielFreak/kurses.py.git
```

### Dependencies
At the moment it is only implemented to work with SDL2 (PySDL2).

```
pip install pysdl2 pysdl2-dll
```

## Examples
### [hello_world.py](examples/hello_world.py)

```python
# load module
from kurses import VirtualTerminal

# instance Virtual console
term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")  # load font resources
stream = term.stream  # get main buffer console


# define loop function
def loop():
    stream.resetall()  # restore default attributes in the buffer console

    # set attributes of first string
    stream.gotoxy(0, 0)  # go to position x: 0, y: 0
    stream.set_background_color((255, 255, 255))  # set background color characters
    stream.set_foreign_color((0, 0, 0))  # set foreign color
    stream.print("Hello\n")  # print into buffer console

    # set attributes of second string
    stream.gotoxy(5, 1)  # go to position x: 5, y: 1
    stream.italic(True)  # set true italic
    stream.print("world!")  # print into buffer console, again


# set loop function
term.set_target(loop)

# run all program
term.main_loop()
```
### [keypressed.py](examples/keypressed.py)

```python
# load modules
import random

from kurses import VirtualTerminal

# instance Virtual console
console = VirtualTerminal("ModernDOS8x16.ttf")
buffer = console.stream  # get buffer console

# define global variables
x, y = 0, 0


# define loop function
def loop():
    global x, y

    buffer.clrscr()
    buffer.resetall()  # restore default attributes in the buffer console

    # check key pressed
    if "w" in console.keyspressed():
        y -= 1
    elif "s" in console.keyspressed():
        y += 1
    if "a" in console.keyspressed():
        x -= 1
    elif "d" in console.keyspressed():
        x += 1

    # all draw runtime of string with random colors
    _x = x

    for _c in "Random color":
        buffer.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        buffer.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        buffer.gotoxy(_x, y)  # set position
        buffer.cputs(_c)  # print character into buffer console
        _x += 1


# set loop function
console.set_target(loop)

# run all program
console.main_loop()
```

### [asteroids.py](examples/asteroids.py)
```python
```

### [testing.py](examples/testing.py)
```python
```