# kurses.py

[![Python - Version](https://img.shields.io/badge/python-%3E%3D3.8-brightgreen)](https://python.org)
[![PyPI - Version](https://img.shields.io/pypi/v/kurses-py?color=green&label=pip%20install%20kurses)](https://pypi.org/project/kurses-py/)
[![Python - Implementation](https://img.shields.io/pypi/implementation/kurses-py)](https://pypi.org/project/kurses-py/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/kurses-py)](https://pypi.org/project/kurses-py/)
[![PyPI - Downloads (for latest version)](https://img.shields.io/pypi/dm/kurses.py)](https://pypi.org/project/kurses.py/)
[![License](https://img.shields.io/pypi/l/kurses.py)](https://github.com/SealtielFreak/kurses.py/blob/main/LICENSE.md)
[![Docs](https://img.shields.io/badge/docs-mkdocs-material-blue)](https://sealtielfreak.github.io/kurses.py/)

> A cross-platform Python module that emulates
> [`conio`](https://en.wikipedia.org/wiki/Conio.h) and
> [`curses`](https://en.wikipedia.org/wiki/Curses_(programming_library))
> using SDL2/Pygame.

`kurses.py` lets you build colorful, styled, text-based user interfaces that
work the same way on Windows, macOS and Linux. You control the color and cursor
of the text, the position and size of the window, the bit depth, the typography
and text styles (underline, bold, italic and strikethrough).

It is designed as a cross-platform solution for creating text applications
independent of the system where they run.

## Features

- **Virtual terminal** with configurable size, title, FPS and hardware/software
  rendering.
- **Text buffers** inspired by `conio`/`curses`: `gotoxy`, `cputs`, `clrscr`,
  colors, bold, italic, underline, strikethrough and more.
- **Multiple buffers** to compose independent screen regions (HUDs, menus,
  split-screen layouts).
- **Bitmap graphics mode** for 2D primitives (lines, rectangles, circles,
  polygons) mixed with text.
- **Audio system** for sound effects, music and synthesized beeps through SDL2
  mixer.
- **Input abstractions** for keyboard, joystick, mouse, touch, battery, gyroscope
  and accelerometer.
- **Event-driven runtime** class for cleaner game-loop architectures.
- **Cross-platform**: Windows, macOS and Linux through SDL2.

## Documentation

Full documentation is built with MkDocs and hosted at
[sealtielfreak.github.io/kurses.py](https://sealtielfreak.github.io/kurses.py/).

You can also serve it locally:

```bash
uv run mkdocs serve
```

## Installation

### From PyPI (recommended)

```bash
pip install "kurses-py[sdl2]"
```

The `[sdl2]` extra installs `pysdl2` and `pysdl2-dll`.

### From source with uv

```bash
git clone https://github.com/SealtielFreak/kurses.py.git
cd kurses.py
uv sync --extra sdl2
```

See the [installation guide](https://sealtielfreak.github.io/kurses.py/getting-started/installation/)
for more options.

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

More examples are available in the [`examples/`](examples/) directory:

- [`hello_world.py`](examples/hello_world.py) — basic styled text.
- [`keypressed.py`](examples/keypressed.py) — keyboard-controlled movement.
- [`testing.py`](examples/testing.py) — colors, styles and rectangles.
- [`virtual_buffer.py`](examples/virtual_buffer.py) — multiple buffers.
- [`audio_demo.py`](examples/audio_demo.py) — sound effects, music and buzzer.
- [`bitmap_demo.py`](examples/bitmap_demo.py) — 2D primitives.
- [`runtime_target_example.py`](examples/runtime_target_example.py) — event-driven runtime.
- [`battery_demo.py`](examples/battery_demo.py) — battery status.
- [`sensors_demo.py`](examples/sensors_demo.py) — gyroscope and accelerometer.
- [`touch_demo.py`](examples/touch_demo.py) — touch input.
- [`asteroids.py`](examples/asteroids.py) — small game combining several features.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency
management.

```bash
# Sync the environment with SDL2 support
uv sync --extra sdl2

# Run the linters and type checker
uv run ruff check .
uv run mypy src/kurses

# Serve the documentation locally
uv run mkdocs serve

# Build the package
uv build
```

## Project layout

```
.
├── docs/                  # MkDocs documentation
├── examples/              # Runnable examples
├── resources/             # Logo and assets
├── src/kurses/            # Package source
│   ├── backend/           # SDL2/Pygame backends
│   ├── events/            # Event-driven runtime
│   ├── font_resources.py  # Font quality / encoding enums
│   ├── graphics/          # Bitmap primitives
│   ├── interface/         # Battery, sensors, joystick, touch
│   ├── resources/         # Audio and buzzer
│   ├── stream/            # Text buffers and attributes
│   ├── surface/           # Texture and bitmap surfaces
│   ├── colors.py          # Color helpers
│   └── term.py            # VirtualTerminal base class
├── pyproject.toml         # Project metadata and tool config
├── mkdocs.yml             # Documentation configuration
├── CHANGELOG.md           # Release notes
└── README.md              # This file
```

## License

This project is released under the LGPL-2.1 license. See
[`LICENSE.md`](LICENSE.md) for details.
