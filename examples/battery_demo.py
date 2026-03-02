# load module
from kurses import VirtualTerminal

# instance Virtual console
term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")  # load font resources
stream = term.stream  # get main buffer console


# define loop function
def loop():
    bat_status, bat_value = term.battery()

    stream.resetall()  # restore default attributes in the buffer console

    # set attributes of first string
    stream.gotoxy(0, 0)  # go to position x: 0, y: 0
    stream.set_background_color((255, 255, 255))  # set background color characters
    stream.set_foreign_color((0, 0, 0))  # set foreign color
    stream.print(f"Battery status: {bat_status}")  # print info

    # set attributes of second string
    stream.gotoxy(0, 1)  # go to position x: 0, y: 1
    stream.italic(True)  # set true italic
    stream.print(f"Battery value: {bat_value}%") # print battery value


# set title of terminal
term.title = "Battery demo"

# set loop function
term.set_target(loop)

# run all program
term.main_loop()
