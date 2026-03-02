# load module
from kurses import VirtualTerminal

# instance Virtual console
term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")  # load font resources
stream = term.stream  # get main buffer console


# define loop function
def loop():
    gyro = term.gyroscope()
    acce = term.accelerometer()

    stream.resetall()

    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))

    stream.gotoxy(0, 0)
    stream.print(f"Gyroscope: {gyro}")

    stream.gotoxy(0, 1)
    stream.print(f"Accelerometer: {acce}")


# set title of terminal
term.title = "Sensors demo (Gyroscope and accelerometer)"

# set loop function
term.set_target(loop)

# run all program
term.main_loop()
