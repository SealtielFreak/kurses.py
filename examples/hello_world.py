# load module
from kurses import Console

# instance Virtual console
console = Console()
buffer = console.buffer  # get buffer console
console.set_font("ModernDOS8x16.ttf")  # load font resources


# define loop function
def loop():
    buffer.resetall()  # restore default attributes in the buffer console

    # set attributes of first string
    buffer.set_background_color((255, 255, 255))  # set background color characters
    buffer.set_foreign_color((0, 0, 0))  # set foreign color
    buffer.print("Hello\n")  # print into buffer console

    # set attributes of second string
    buffer.gotoxy(5, 1)  # go to position x: 5, y: 1
    buffer.italic(True)  # set true italic
    buffer.print("world!")  # print into buffer console, again


# set loop function
console.set_target(loop)

# run all program
console.main_loop()
