from pyrlkit import Console


if __name__ == "__main__":
    console = Console()
    term = console.buffer

    def main():
        while True:
            term.print("Hello world")

    console.set_target(main)
    console.main_loop()
