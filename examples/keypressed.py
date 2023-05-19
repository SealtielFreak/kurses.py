# load modules
from kurses import Console
import random

# instance Virtual console
console = Console()
buffer = console.buffer  # get buffer console
console.set_font("ModernDOS8x16.ttf")  # load font resources

# define global variables
x, y = 0, 0


# define loop function
def loop():
    global x, y

    term = console.buffer

    buffer.resetall()  # restore default attributes in the buffer console

    # check key pressed
    if "w" in console.keyspressed():
        y -= 1
    elif "s" in console.keyspressed():
        y += 1
    if "a" in console.keyspressed():
        x -= 1
    elif "d" in console.keyspressed():
        x += 1

    # all draw runtime of string with random colors
    _x = x
    for _c in "Random color":
        term.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        term.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        term.gotoxy(_x, y) # set position
        term.cputs(_c) # print character into buffer console
        _x += 1


# set loop function
console.set_target(loop)

# run all program
console.main_loop()
