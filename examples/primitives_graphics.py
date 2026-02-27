import typing

from kurses import VirtualTerminal
from kurses.events import EventTargetRuntime
from kurses.interface.joystick import JoystickInput

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

        graphics.circle(0, 0, 59, (255, 0, 0), filled=True)
        graphics.polygon([400, 100, 500, 300, 300, 300], (255, 0, 255), filled=True)
        graphics.line([0, 0], [width, height], (255, 0, 0), thickness=10)
        graphics.circle(x, y, 15, (255, 255, 0), filled=False)
        graphics.rect(0, 0, (10, 10), (0, 255, 0), filled=True)
        graphics.rect(10, 10, (10, 10), (0, 255, 0), filled=False)

        term.purge()

    def mouse(self, click: int, position, motion):
        self.position = motion

    def joystick(self, inputs: typing.Tuple[JoystickInput, ...]):
        print(inputs)


if __name__ == "__main__":
    term.title = "Primitives graphics"
    term.set_runtime(PrimitiveGraphicsDemo)

    term.main_loop()
