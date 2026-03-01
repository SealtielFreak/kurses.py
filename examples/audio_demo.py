# load module
from kurses import VirtualTerminal, Effect, Music

# instance Virtual console
term = VirtualTerminal(font_filename="./ModernDOS8x16.ttf", sound_enabled=True)  # load font resources
stream = term.stream  # get main buffer console
buzzer = term.buzzer # get main buzzer console

# Create tracks for buzzer
buzzer.record(0, [(440, 200), (493, 200), (523, 200), (587, 400)])

# Load sound effect
effect = Effect(filename="./laser.mp3")
effect.volume(10)

# Load music
music = Music(filename="./win95.mp3")
music.volume(15)

music.play(2)
music.fadeout(5)

# define loop function
def loop():
    stream.resetall()  # restore default attributes in the buffer console

    # set attributes of first string
    stream.gotoxy(0, 0)  # go to position x: 0, y: 0
    stream.set_background_color((255, 255, 255))  # set background color characters
    stream.set_foreign_color((0, 0, 0))  # set foreign color
    stream.print("Sounds\n")  # print into buffer console

    # set attributes of second string
    stream.gotoxy(5, 1)  # go to position x: 5, y: 1
    stream.italic(True)  # set true italic
    stream.print("in Kurses!")  # print into buffer console, again

    keys = term.keyspressed()

    if "space" in keys:
        effect.play(2)

    if "w" in keys:
        buzzer.play(0, 25)

    if "s" in keys:
        buzzer.beep(440, 25, 25)



# set loop function
term.set_target(loop)

# run all program
term.main_loop()
