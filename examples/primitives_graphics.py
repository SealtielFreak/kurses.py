from kurses import VirtualTerminal
from kurses.events import EventTargetRuntime

term = VirtualTerminal(font_filename="./ModernDOS8x16.ttf")
stream = term.stream
graphics = term.graphics


class PrimitiveGraphicsDemo(EventTargetRuntime):
    def __init__(self):
        self.position = 0, 0

    def load(self):
        term.resizable = True
        stream.resetall()

    def update(self, dt):
        x, y = self.position
        width, height = term.size

        # graphics.circle(0, 0, 59, (255, 0, 0), filled=True)
        graphics.polygon([400, 100, 500, 300, 300, 300], (255, 0, 255), filled=True)
        graphics.line([0, 0], [width, height], (255, 0, 0), thickness=10)
        graphics.circle(x, y, 15, (255, 255, 0), filled=False)

        term.purge()

    def key_down(self, key: chr):
        print(f"Key down: {key}")

    def key_up(self, key: chr):
        print(f"Key up: {key}")

    def mouse(self, click: int, position, motion):
        self.position = motion

    def exit(self):
        stream.resetall()
        stream.gotoxy(0, 0)
        stream.set_foreign_color((255, 255, 255))
        stream.print("Goodbye")


if __name__ == "__main__":
    term.title = "Primitives graphics"
    term.set_runtime(PrimitiveGraphicsDemo)

    term.main_loop()
