# API Reference

This section contains auto-generated documentation for every public module,
class, function and type alias exposed by `kurses.py`.

The package is organized into several layers:

| Layer | Description |
|-------|-------------|
| [`kurses.term`](terminal.md) | [`VirtualTerminal`][kurses.term.VirtualTerminal] and rendering modes. |
| [`kurses.stream`](stream.md) | Text buffers, character attributes and cursor types. |
| [`kurses.graphics`](graphics.md) | Bitmap graphics primitives and buffer. |
| [`kurses.events`](events.md) | Event-driven runtime classes. |
| [`kurses.resources`](audio.md) | Audio abstractions: sound, music, effects and buzzer. |
| [`kurses.interface`](interfaces.md) | Joystick, battery, sensors and touch types. |
| [`kurses.colors` / `kurses.font_resources`](utilities.md) | Color helpers and font quality enums. |

!!! note
    The SDL2 backend (`kurses.backend.sdl2.*`) is the concrete implementation
    selected when PySDL2 is installed. The public API imported from
    `kurses` is the same across backends.
