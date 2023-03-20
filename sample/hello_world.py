from pyrlkit import Console


if __name__ == "__main__":
    console = Console()
    term = console.buffer

    def main():
        while True:
            term.cputsxy(0, 0, "Hello world")

    console.set_target(main)
    console.main_loop()
