# kurses.py

This module uses SDL2 (or Pygame) to emulate the functions of the
[`conio`](https://en.wikipedia.org/wiki/Conio.h) and
[`curses`](https://en.wikipedia.org/wiki/Curses_(programming_library))
libraries, which are used to create text-based user interfaces. You can control
the color and cursor of the text, as well as the position and size of the
window, the bit depth, typography and text styles (underline, bold, italic and
strikethrough).

It is designed to offer a cross-platform solution for creating text-based
applications, independent of the system where they run.

## How to install it?

With `uv`:

```bash
uv pip install kurses-py
```

Or with `pip`:

```bash
pip install kurses-py
```

### Dependencies

At the moment it is only implemented to work with SDL2 (PySDL2). Install the
optional SDL2 extra:

```bash
uv pip install "kurses-py[sdl2]"
```

## Quick start

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    stream.resetall()
    stream.gotoxy(0, 0)
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))
    stream.print("Hello\n")

    stream.gotoxy(5, 1)
    stream.italic(True)
    stream.print("world!")


term.set_target(loop)
term.main_loop()
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency
management.

```bash
# Sync the environment with SDL2 support
uv sync --extra sdl2

# Run linters and type checker
uv run ruff check .
uv run mypy src/kurses

# Build the documentation
uv run mkdocs serve
```
