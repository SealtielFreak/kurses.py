# Colors and Styles

`kurses.py` lets you apply foreground and background colors as well as text
styles such as bold, italic, underline and strikethrough.

## What you will learn

- How to use [`bold()`][kurses.stream.StreamBuffer.bold],
  [`italic()`][kurses.stream.StreamBuffer.italic],
  [`underline()`][kurses.stream.StreamBuffer.underline] and
  [`strikethrough()`][kurses.stream.StreamBuffer.strikethrough].
- How to draw solid rectangles with [`putrect()`][kurses.stream.StreamBuffer.putrect].
- How to combine styles on the same buffer.

## Complete example

```python
import random

from kurses import VirtualTerminal
from kurses.term import Rendering

console = VirtualTerminal("ModernDOS8x16.ttf", type_rendering=Rendering.HARDWARE)
console.resizable = True

x, y = 0, 0


def main():
    global x, y

    term = console.streams[0]
    term.clrscr()

    if "w" in console.keyspressed():
        y -= 1
    elif "s" in console.keyspressed():
        y += 1
    if "a" in console.keyspressed():
        x -= 1
    elif "d" in console.keyspressed():
        x += 1

    term.resetall()
    term.set_background_color((0, 255, 0))
    term.set_foreign_color((225, 23, 155))
    term.putrect(0, 0, 5, 30)
    term.cputsxy(0, 0, "Hello world")

    term.italic(True)
    term.bold(True)
    term.set_background_color((255, 255, 255))
    term.set_foreign_color((0, 0, 0))
    term.cputsxy(6, 1, "Italic and bold text")

    term.resetall()
    term.underline(True)
    term.cputsxy(16, 16, "Underline text")

    term.resetall()
    term.strikethrough(True)
    term.set_foreign_color((255, 0, 0))
    term.cputsxy(24, 24, "Strikethrough text")

    term.resetall()
    _x = x
    for _c in "Random color":
        term.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        term.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        term.gotoxy(_x, y)
        term.cputs(_c)
        _x += 1


console.set_target(main)
console.main_loop()
```

## Breaking it down

### Text styles

```python
term.italic(True)
term.bold(True)
```

Styles are enabled by passing `True` and disabled with `False` or by calling
[`resetall()`][kurses.stream.StreamBuffer.resetall].

### Solid rectangles

```python
term.set_background_color((0, 255, 0))
term.putrect(0, 0, 5, 30)
```

[`putrect(x, y, w, h)`][kurses.stream.StreamBuffer.putrect] draws a filled
rectangle using the current background color.

### Resizable terminal

```python
console.resizable = True
```

When enabled, the logical buffer is resized automatically when the window is
resized.

## Try it

Experiment by stacking multiple styles at once, for example bold + italic +
colored background.

## Next tutorial

Render independent screen regions in [Virtual Buffers](virtual-buffers.md).
