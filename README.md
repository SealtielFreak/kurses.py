![Alt text](kurses.png)
# What is kurses?
This module uses SDL2 (or Pygame) to emulate the functions of the [conio](https://en.wikipedia.org/wiki/Conio.h) and [curses](https://en.wikipedia.org/wiki/Curses_(programming_library)) libraries, which are used to create text-based user interfaces. You can control the color and cursor of the text, as well as the position and size of the window, the bit depth, typography and text styles (underline, bold, italic and strikethrough).

It is designed to offer a cross-platform solution for creating text-based applications, independent of the system where they run.

## How to install it?
`pip install kurses-py`

## Dependencies
At the moment it is only implemented to work with SDL2 (PySDL2).

`pip install pysdl2 pysdl2-dll`

# Examples
[hello_world.py](examples/hello_world.py)
```python
# load module
from kurses import Console

# instance Virtual console
console = Console()
buffer = console.buffer  # get buffer console
console.set_font("ModernDOS8x16.ttf")  # load font resources


# define loop function
def loop():
    # set attributes of first string
    buffer.set_background_color((255, 255, 255))  # set background color characters
    buffer.set_foreign_color((0, 0, 0))  # set foreign color
    buffer.print("Hello\n")  # print into buffer console

    # set attributes of second string
    buffer.gotoxy(5, 1)  # go to position x: 5, y: 1
    buffer.italic(True)  # set true italic
    buffer.print("world!")  # print into buffer console, again

    buffer.resetall()  # restore default attributes in the buffer console


# set loop function
console.set_target(loop)

# run all program
console.main_loop()
```
[keypressed.py](examples/keypressed.py)
```python
# load modules
from kurses import Console
import random

# instance Virtual console
console = Console()
buffer = console.buffer  # get buffer console
console.set_font("ModernDOS8x16.ttf")  # load font resources

# define global variables
x, y = 0, 0


# define loop function
def loop():
    global x, y

    term = console.buffer

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
        term.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        term.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        term.gotoxy(_x, y) # set position
        term.cputs(_c) # print character into buffer console
        _x += 1


# set loop function
console.set_target(loop)

# run all program
console.main_loop()

```
