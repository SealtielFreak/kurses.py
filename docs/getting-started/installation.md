# Installation

`kurses.py` is published on PyPI as `kurses-py`. The runtime only requires
`numpy`, but the actual rendering and audio backends need SDL2 bindings.

## Requirements

- Python 3.8 or newer.
- A working SDL2 runtime (the `pysdl2-dll` package usually provides it).
- A TrueType or bitmap font file for rendering text (the examples use
  `ModernDOS8x16.ttf`).

## Install from PyPI

### With SDL2 support (recommended)

```bash
pip install "kurses-py[sdl2]"
```

The `[sdl2]` extra installs `pysdl2` and `pysdl2-dll` for you.

### Runtime only

If you already manage SDL2 yourself:

```bash
pip install kurses-py
pip install pysdl2 pysdl2-dll
```

## Install from source with uv

This project uses [uv](https://docs.astral.sh/uv/) for development.

```bash
git clone https://github.com/SealtielFreak/kurses.py.git
cd kurses.py
uv sync --extra sdl2
```

The command above creates a local virtual environment (`.venv/`), installs the
package in editable mode and pulls every development dependency (ruff, mypy,
pytest, mkdocs, etc.).

## Verify the installation

Run the bundled hello-world example:

```bash
uv run examples/hello_world.py
```

If a window opens and shows *Hello world!*, everything is ready.

!!! tip
    When running examples directly, make sure your terminal's working
    directory is the repository root so the font path (`ModernDOS8x16.ttf`)
    resolves correctly.
