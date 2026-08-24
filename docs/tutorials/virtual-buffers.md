# Virtual Buffers

A single terminal can render more than one [`StreamBuffer`][kurses.stream.StreamBuffer].
This is useful for split-screen layouts, HUDs, menus or layered consoles.

## What you will learn

- How to create additional [`StreamBuffer`][kurses.stream.StreamBuffer] instances.
- How to configure cursor types with [`TypeCursor`][kurses.stream.attributes.TypeCursor].
- How to append buffers to [`term.streams`][kurses.term.VirtualTerminal.streams].

## Complete example

```python
import kurses.stream
from kurses import StreamBuffer, VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
buffer_0 = term.stream
buffer_1 = StreamBuffer(80, 30, sx=2, sy=2)

buffer_0.type_cursor = kurses.stream.TypeCursor.VERTICAL
buffer_1.type_cursor = kurses.stream.TypeCursor.VERTICAL


def loop():
    buffer_1.resetall()

    buffer_0.gotoxy(10, 2)
    buffer_0.italic(True)
    buffer_0.print("world!")

    buffer_1.gotoxy(0, 0)
    buffer_1.set_background_color((255, 255, 255))
    buffer_1.set_foreign_color((0, 0, 0))
    buffer_1.print("Hello")


term.streams.append(buffer_1)
term.set_target(loop)
term.main_loop()
```

## Breaking it down

### Create an extra buffer

```python
buffer_1 = StreamBuffer(80, 30, sx=2, sy=2)
```

`StreamBuffer(columns, rows, ...)` creates a secondary buffer. `sx` and `sy`
control the horizontal and vertical scale of its characters.

### Choose a cursor style

```python
buffer_0.type_cursor = kurses.stream.TypeCursor.VERTICAL
```

[`TypeCursor`][kurses.stream.attributes.TypeCursor] offers several styles:
`LINE`, `RECT`, `SOLID_RECT`, `VERTICAL`, `UNDERSCORE` and `EMPTY`.

### Register the buffer

```python
term.streams.append(buffer_1)
```

All buffers in [`term.streams`][kurses.term.VirtualTerminal.streams] are
rendered each frame. The main buffer is always the first one.

## Try it

Create a small HUD buffer and a large world buffer. Update each independently in
the same loop.

## Next tutorial

Add sound effects and music in [Audio](audio.md).
