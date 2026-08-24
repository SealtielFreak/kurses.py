# Graphics

The graphics layer provides a queue of 2D primitives that can be rendered on
top of the text buffer when bitmap mode is enabled.

## kurses.graphics

::: kurses.graphics
    options:
      members:
        - GraphicsBuffer

## kurses.graphics.primitive

::: kurses.graphics.primitive
    options:
      members:
        - PrimitiveFigure
        - LineFigure
        - RectangleFigure
        - CircleFigure
        - PolygonFigure
