from pyrogue import Console


if __name__ == "__main__":
    console = Console()
    term = console.buffer

    def main():
        print(console.keyspressed())

        term.set_background_color((0, 255, 0))
        term.set_foreign_color((255, 0, 255))
        term.cputsxy(0, 0, "Hello world")

        term.set_background_color((255, 0, 0))
        term.set_foreign_color((0, 255, 255))
        term.cputsxy(6, 1, "Hello world")

        # term.set_background_color((0, 0, 0))

        term.resetall()

    console.set_target(main)
    console.main_loop()

    exit()
