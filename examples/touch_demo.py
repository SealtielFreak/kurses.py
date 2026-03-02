# load module
from kurses import VirtualTerminal

# instance Virtual console
term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")  # load font resources
stream = term.stream  # get main buffer console


# define loop function
def loop():
    stream.resetall()

    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))

    for i, (x, y) in term.touch():
        stream.gotoxy(x, y)
        stream.print(f"Finger[{i}]: x={x}, y={y}")


# set title of terminal
term.title = "Touchscreen demo"

# set loop function
term.set_target(loop)

# run all program
term.main_loop()
