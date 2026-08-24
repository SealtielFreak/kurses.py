# Touch Input

On touch-capable devices, `kurses.py` reports active fingers through the
`touch()` method.

## What you will learn

- How to iterate over active touch points.
- How to map touch positions to the logical grid.

## Complete example

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    stream.resetall()
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))

    for i, (x, y) in term.touch():
        stream.gotoxy(x, y)
        stream.print(f"Finger[{i}]: x={x}, y={y}")


term.title = "Touchscreen demo"
term.set_target(loop)
term.main_loop()
```

## Breaking it down

### Read touches

```python
for i, (x, y) in term.touch():
    ...
```

`touch()` returns a list of `(finger_id, (x, y))` tuples. The coordinates are
normalized to the logical buffer grid.

### Draw per finger

```python
stream.gotoxy(x, y)
stream.print(f"Finger[{i}]: x={x}, y={y}")
```

You can assign a different color to each finger or draw a cursor under every
active touch point.

## Try it

Track multiple fingers and draw a colored trail for each one.

## Next tutorial

Put everything together in a small game with [Asteroids](../graphics/asteroids.md).
