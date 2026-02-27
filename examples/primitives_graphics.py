import random

from kurses import VirtualTerminal
from kurses.font_resources import QualityFont
from kurses.graphics import GraphicsBuffer

console = VirtualTerminal(font_filename="./ModernDOS8x16.ttf", quality=QualityFont.SOLID)
buffer = console.stream
graphics = console.graphics

buffer.cputsxy(0, 0, "Hello world")

width, height = console.size
position = [width // 2, height // 2]
speed = [
    random.randint(-5, 5), random.randint(-5, 5)
]

graphics.circle(0, 0, 59, (255, 0, 0))

def loop():
    global position, speed

    sx, sy = speed
    x, y = position

    graphics.circle(x, y, 15, (255, 255, 0))

    if x > width or x < 0:
        sx *= -1

    x += sx

    if y > height or y < 0:
        sy *= -1

    y += sy

    position = [x, y]
    speed = [sx, sy]

    console.purge()


if __name__ == "__main__":
    console.title = "Primitives graphics"
    console.set_target(loop)
    console.main_loop()
