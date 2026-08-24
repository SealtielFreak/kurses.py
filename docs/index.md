# kurses.py

[![Python - Version](https://img.shields.io/badge/python-%3E%3D3.8-brightgreen)](https://python.org)
[![PyPI - Version](https://img.shields.io/pypi/v/kurses-py?color=green&label=pip%20install%20kurses)](https://pypi.org/project/kurses-py/)
[![License](https://img.shields.io/pypi/l/kurses.py)](https://github.com/SealtielFreak/kurses.py/blob/main/LICENSE.md)

**kurses.py** is a Python module that emulates the classic
[`conio`](https://en.wikipedia.org/wiki/Conio.h) and
[`curses`](https://en.wikipedia.org/wiki/Curses_(programming_library))
libraries on top of SDL2 (via PySDL2). It lets you build colorful, styled,
text-based user interfaces that run cross-platform without relying on a real
terminal.

Whether you want to prototype a retro console UI, draw text with custom bitmap
fonts, play sound effects and music, read joysticks, or even render 2D
primitives, `kurses.py` gives you a single, familiar API to do it all.

## Features

- **Virtual terminal** with configurable size, title, FPS and hardware/software
  rendering.
- **Text buffers** inspired by `conio`/`curses`: `gotoxy`, `cputs`, `clrscr`,
  colors, bold, italic, underline, strikethrough, and more.
- **Multiple buffers** to compose independent screen regions.
- **Bitmap graphics mode** for 2D primitives (lines, rectangles, circles,
  polygons) mixed with text.
- **Audio system** for sound effects and music through SDL2 mixer.
- **Joystick**, **sensor**, **battery** and **touch** input abstractions.
- **Event-driven runtime** class for cleaner game-loop architectures.
- **Cross-platform**: Windows, macOS and Linux through SDL2.

## Quick example

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    stream.resetall()
    stream.gotoxy(0, 0)
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))
    stream.print("Hello")

    stream.gotoxy(5, 1)
    stream.italic(True)
    stream.print("world!")


term.set_target(loop)
term.main_loop()
```

## Where to go next

- [Install kurses.py](getting-started/installation.md) — `pip`, `uv` and SDL2
  setup.
- [Quickstart](getting-started/quickstart.md) — create your first window and
  understand the loop.
- [Tutorials](tutorials/hello-world.md) — step-by-step guides based on the
  bundled examples.
- [API Reference](api/index.md) — auto-generated docs for every module, class
  and function.
- [Changelog](changelog.md) — release history and breaking changes.
