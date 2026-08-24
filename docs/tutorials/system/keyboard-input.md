# Keyboard Input

This tutorial shows how to read the keyboard and move a colored string around
the screen.

## What you will learn

- How to poll keys with [`keyspressed()`][kurses.term.VirtualTerminal.keyspressed].
- How to clear the screen each frame with [`clrscr()`][kurses.stream.StreamBuffer.clrscr].
- How to draw a string one character at a time.

## Complete example

```python
import random

from kurses import VirtualTerminal

console = VirtualTerminal("ModernDOS8x16.ttf")
buffer = console.stream

x, y = 0, 0


def loop():
    global x, y

    buffer.clrscr()
    buffer.resetall()

    if "w" in console.keyspressed():
        y -= 1
    elif "s" in console.keyspressed():
        y += 1
    if "a" in console.keyspressed():
        x -= 1
    elif "d" in console.keyspressed():
        x += 1

    _x = x
    for _c in "Random color":
        buffer.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        buffer.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        buffer.gotoxy(_x, y)
        buffer.cputs(_c)
        _x += 1


console.set_target(loop)
console.main_loop()
```

## Breaking it down

### Poll the keyboard

```python
keys = console.keyspressed()
```

[`keyspressed()`][kurses.term.VirtualTerminal.keyspressed] returns a list of
lowercase key names currently held down. Common names include `"w"`, `"a"`,
`"s"`, `"d"`, `"space"`, `"return"`, `"escape"`.

### Clear the screen

```python
buffer.clrscr()
```

Unlike [`resetall()`][kurses.stream.StreamBuffer.resetall], which only resets
attributes, [`clrscr()`][kurses.stream.StreamBuffer.clrscr] empties the queued
characters so the previous frame disappears.

### Move the text

```python
if "w" in keys:
    y -= 1
```

We update `x` and `y` based on the pressed keys, then redraw the string at the
new position.

## Try it

Use `W`, `A`, `S`, `D` to move the rainbow text around the terminal.

## Next tutorial

Learn about bold, italic, underline and other styles in
[Colors and Styles](../graphics/colors-styles.md).
