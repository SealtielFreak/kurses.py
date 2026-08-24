# Hello World

The classic first program: open a virtual terminal and print styled text at
specific positions.

## What you will learn

- How to create a [`VirtualTerminal`][kurses.term.VirtualTerminal].
- How to get the main [`StreamBuffer`][kurses.stream.StreamBuffer].
- How to move the cursor, set colors and print text.
- How to set the loop target and run [`main_loop()`][kurses.term.VirtualTerminal.main_loop].

## Complete example

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    stream.resetall()

    # First line: white background, black text
    stream.gotoxy(0, 0)
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))
    stream.print("Hello")

    # Second line: italic at (5, 1)
    stream.gotoxy(5, 1)
    stream.italic(True)
    stream.print("world!")


term.set_target(loop)
term.main_loop()
```

## Breaking it down

### Create the terminal

```python
term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
```

The font file must exist in the working directory or be given as an absolute
path. `VirtualTerminal` initializes SDL2, creates the window and prepares the
main text buffer.

### Get the stream buffer

```python
stream = term.stream
```

`term.stream` is the primary [`StreamBuffer`][kurses.stream.StreamBuffer] where
text, colors and styles are queued before rendering.

### Position and colors

```python
stream.gotoxy(0, 0)
stream.set_background_color((255, 255, 255))
stream.set_foreign_color((0, 0, 0))
```

- [`gotoxy(x, y)`][kurses.stream.StreamBuffer.gotoxy] sets the logical cursor
  position in columns and rows.
- [`set_background_color`][kurses.stream.StreamBuffer.set_background_color]
  changes the background RGB color.
- [`set_foreign_color`][kurses.stream.StreamBuffer.set_foreign_color] changes
  the foreground RGB color.

### Reset attributes

```python
stream.resetall()
```

Always call [`resetall()`][kurses.stream.StreamBuffer.resetall] at the top of
your loop to avoid styles leaking from the previous frame.

## Try it

Save the code as `hello.py` next to a font file and run:

```bash
uv run hello.py
```

## Next tutorial

Add movement and keyboard control in [Keyboard Input](../system/keyboard-input.md).
