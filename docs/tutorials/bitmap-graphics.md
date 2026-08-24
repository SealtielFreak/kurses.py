# Bitmap Graphics

`kurses.py` includes an experimental bitmap graphics mode that lets you draw
primitives such as lines, rectangles, circles and polygons alongside text.

## What you will learn

- How to enable bitmap mode with `bitmap_enabled=True`.
- How to choose between hardware and software rendering.
- How to use the [`GraphicsBuffer`][kurses.graphics.GraphicsBuffer] API.

## Complete example

```python
from kurses import VirtualTerminal
from kurses.term import Rendering

term = VirtualTerminal(
    font_filename="./ModernDOS8x16.ttf",
    rendering=Rendering.SOFTWARE,
    bitmap_enabled=True,
)
stream = term.stream
graphics = term.graphics

stream.cputsxy(40, 20, "Hello World")


def loop():
    state, _, (x, y) = term.mouse()
    width, height = term.size

    graphics.circle(0, 0, 59, (255, 0, 0), filled=True)
    graphics.polygon([400, 100, 500, 300, 300, 300], (255, 0, 255), filled=True)
    graphics.line([0, 0], [width, height], (255, 0, 0), thickness=10)
    graphics.circle(x, y, 15, (255, 255, 0), filled=False)
    graphics.rect(0, 0, (10, 10), (0, 255, 0), filled=True)
    graphics.rect(10, 10, (10, 10), (0, 255, 0), filled=False)

    term.purge()


if __name__ == "__main__":
    term.title = "Primitives graphics"
    term.set_target(loop)
    term.main_loop()
```

## Breaking it down

### Enable bitmap mode

```python
term = VirtualTerminal(
    font_filename="./ModernDOS8x16.ttf",
    rendering=Rendering.SOFTWARE,
    bitmap_enabled=True,
)
```

Bitmap mode is experimental and must be explicitly enabled. It currently works
best with `Rendering.SOFTWARE`.

### Get the graphics buffer

```python
graphics = term.graphics
```

If bitmap mode is disabled, accessing `term.graphics` raises a `RuntimeError`.

### Draw primitives

```python
graphics.circle(0, 0, 59, (255, 0, 0), filled=True)
graphics.line([0, 0], [width, height], (255, 0, 0), thickness=10)
graphics.rect(0, 0, (10, 10), (0, 255, 0), filled=True)
graphics.polygon([400, 100, 500, 300, 300, 300], (255, 0, 255), filled=True)
```

Shapes are queued and rendered on top of the text layer. Colors are RGB tuples.

### Clear the bitmap

```python
term.purge()
```

[`purge()`][kurses.term.VirtualTerminal.purge] clears the graphics queue so the
next frame starts fresh. Without it, shapes accumulate indefinitely.

## Try it

Draw a moving rectangle that follows the mouse cursor.

## Next tutorial

Build a cleaner architecture with [Runtime Events](runtime-events.md).
