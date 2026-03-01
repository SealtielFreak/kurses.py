from kurses import VirtualTerminal
from kurses.term import Rendering

term = VirtualTerminal(font_filename="./ModernDOS8x16.ttf", rendering=Rendering.SOFTWARE, bitmap_enabled=False)
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
