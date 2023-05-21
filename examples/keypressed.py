# load modules
from kurses import Console
import random

# instance Virtual console
console = Console()
buffer = console.buffers[0]  # get buffer console
console.set_font("ModernDOS8x16.ttf")  # load font resources

# define global variables
x_ship, y_ship = 0, 0


# define loop function
def loop():
    global x_ship, y_ship

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
        buffer.set_foreign_color(tuple(random.randint(0, 255) for _ in range(3)))
        buffer.set_background_color(tuple(random.randint(0, 255) for _ in range(3)))
        buffer.gotoxy(_x, y) # set position
        buffer.cputs(_c) # print character into buffer console
        _x += 1


# set loop function
console.set_target(loop)

# run all program
console.main_loop()
