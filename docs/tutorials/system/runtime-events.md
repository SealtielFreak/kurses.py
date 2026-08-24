# Runtime Events

Instead of a plain callback, you can implement an
[`EventTargetRuntime`][kurses.events.EventTargetRuntime] subclass. This keeps
input, update and rendering logic organized in one place.

## What you will learn

- How to subclass [`EventTargetRuntime`][kurses.events.EventTargetRuntime].
- How to handle keyboard, mouse and resize events.
- How to register the runtime with `set_runtime()`.

## Complete example

```python
import random
import typing

from kurses import VirtualTerminal
from kurses.events import EventTargetRuntime

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


class MyTarget(EventTargetRuntime):
    def __init__(self):
        self.position = 0, 0

    def load(self):
        term.resizable = True
        stream.resetall()

    def update(self, dt):
        x, y = self.position

        stream.clrscr()

        stream.gotoxy(x, y)
        stream.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        stream.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        stream.print("Hello\n")

        stream.gotoxy(x + 5, y + 1)
        stream.italic(True)
        stream.print("world!")

    def key_down(self, key: str):
        print(f"Key down: {key}")

    def key_up(self, key: str):
        print(f"Key up: {key}")

    def mouse(self, click, position: typing.Tuple[int, int], motion: typing.Tuple[int, int]):
        self.position = position

    def exit(self):
        stream.resetall()
        stream.gotoxy(0, 0)
        stream.set_foreign_color((255, 255, 255))
        stream.print("Goodbye")


if __name__ == "__main__":
    term.set_runtime(MyTarget)
    term.main_loop()
```

## Breaking it down

### Subclass EventTargetRuntime

```python
class MyTarget(EventTargetRuntime):
    def update(self, dt):
        ...
```

Only [`update(dt)`][kurses.events.EventTargetRuntime.update] is abstract; the
rest are optional hooks.

### Lifecycle hooks

- [`load()`][kurses.events.EventTargetRuntime.load] runs once before the loop.
- [`update(dt)`][kurses.events.EventTargetRuntime.update] runs every frame.
- [`draw()`][kurses.events.EventTargetRuntime.draw] runs after update.
- [`exit()`][kurses.events.EventTargetRuntime.exit] runs when the window closes.

### Input hooks

```python
def key_down(self, key: str):
    print(f"Key down: {key}")

def mouse(self, click, position, motion):
    self.position = position
```

[`mouse(click, position, motion)`][kurses.events.EventTargetRuntime.mouse]
receives the clicked buttons, the logical grid position and the raw pixel
motion.

### Register the runtime

```python
term.set_runtime(MyTarget)
term.main_loop()
```

Pass the class (not an instance) to `set_runtime()`.
The terminal instantiates it internally.

## Try it

Extend the example with [`resize()`][kurses.events.EventTargetRuntime.resize] to
recenter text after the window is resized.

## Next tutorial

Read hardware sensors in [Sensors and Battery](../sensors/sensors-battery.md).
