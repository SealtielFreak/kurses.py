# Quickstart

This guide walks you through the core concepts of `kurses.py`: creating a
virtual terminal, writing to a stream buffer, and running the main loop.

## The virtual terminal

The [`VirtualTerminal`][kurses.term.VirtualTerminal] class is the entry point.
It creates an SDL2 window, manages events, and exposes subsystems such as the
main text buffer, audio, graphics and input.

```python
from kurses import VirtualTerminal

term = VirtualTerminal(
    font_filename="ModernDOS8x16.ttf",  # required font file
    shape=(80, 30),                     # logical columns and rows
    size=(640, 480),                    # window pixel size
    title="My first kurses app",
    fps=30,
)
```

## The stream buffer

Every terminal owns a main [`StreamBuffer`][kurses.stream.StreamBuffer] that
stores characters, colors and styles. Use it like a classic `conio` console:

```python
stream = term.stream

stream.resetall()                       # reset colors and styles
stream.gotoxy(10, 5)                    # move cursor
stream.set_foreign_color((0, 255, 0))   # green text
stream.print("Hello from kurses.py!")
```

## The main loop

`kurses.py` uses a callback-based loop. You define a function that is called
once per frame, then hand it to the terminal and call
[`main_loop()`][kurses.term.VirtualTerminal.main_loop].

```python
def loop():
    stream.clrscr()
    stream.resetall()
    stream.gotoxy(10, 5)
    stream.print("Press ESC to close")


term.set_target(loop)
term.main_loop()
```

The loop continues until the window is closed or you call
[`term.quit()`][kurses.term.VirtualTerminal.quit].

## Reading input

Use [`keyspressed()`][kurses.term.VirtualTerminal.keyspressed] to poll the
keyboard:

```python
def loop():
    stream.clrscr()
    stream.print(f"Keys: {term.keyspressed()}")
```

Keys are returned as lowercase strings, e.g. `"space"`, `"return"`, `"w"`,
`"escape"`.

## Full quickstart example

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    stream.clrscr()
    stream.resetall()
    stream.gotoxy(0, 0)
    stream.print("kurses.py quickstart")
    stream.gotoxy(0, 2)
    stream.print(f"Keys: {term.keyspressed()}")


term.set_target(loop)
term.main_loop()
```

## Next steps

- Learn the text API in depth with the [Hello World](../tutorials/hello-world.md)
  and [Colors and Styles](../tutorials/colors-styles.md) tutorials.
- Add movement with [Keyboard Input](../tutorials/keyboard-input.md).
- Explore the [API Reference](../api/index.md) for every class and method.
