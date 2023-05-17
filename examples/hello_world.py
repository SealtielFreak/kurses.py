from kurses import Console


console = Console()
console.set_font("ModernDOS8x16.ttf")


def loop():
    console.buffer.set_background_color((255, 255, 255))
    console.buffer.set_foreign_color((0, 0, 0))

    console.buffer.print("Hello\n")

    console.buffer.gotoxy(5, 1)
    console.buffer.italic(True)
    console.buffer.print("world!")

    console.buffer.resetall()


console.set_target(loop)
console.main_loop()
