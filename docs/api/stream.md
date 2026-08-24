# Stream Buffer

Text buffers store characters, colors, styles and cursor state. They are the
heart of the `conio`/`curses`-like API.

## kurses.stream

::: kurses.stream
    options:
      members:
        - StreamBuffer
        - TypeCursor

## kurses.stream.buffer

::: kurses.stream.buffer
    options:
      members:
        - BufferMatrix
        - fix_position_attribute
        - protect_buffer_matrix

## kurses.stream.attributes

::: kurses.stream.attributes
    options:
      members:
        - Attribute
        - CharacterAttribute
        - RectangleAttribute
        - TypeCursor
