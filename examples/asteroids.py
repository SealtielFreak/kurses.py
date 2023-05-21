import math
import random

import kurses.virtual_console


SHIP = """\
 |
/0\\
"""


def draw_ship(x, y, buffer):
    buffer.set_foreign_color((255, 0, 255))
    buffer.gotoxy(x, y)
    buffer.print(SHIP)
    buffer.resetall()


def random_asteroid(_x=(0, 80), _y=(0, 30)):
    return (
        random.randint(*_x),
        random.randint(*_y),
        random.randint(1, 2),
        random.sample([(255, 255, 255), (255, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 0), (0, 255, 0)], 1)[0],
        random.sample("*", 1)[0],
    )


console = kurses.Console(quality=kurses.virtual_console.QualityFont.LCD)
buffer = console.buffer

life, score = 100, 0
x, y = random.randint(0, 70), random.randint(0, 30)
shoots = []
asteroids = [random_asteroid() for _ in range(15)]


def loop():
    global x, y, life, score
    rows, columns = buffer.buffersize

    if life > 0:
        if "w" in console.keyspressed() and y >= 0:
            y -= 1
        elif "s" in console.keyspressed() and y <= rows - 3:
            y += 1

        if "a" in console.keyspressed() and x >= 0:
            x -= 1
        elif "d" in console.keyspressed() and x <= columns - 3:
            x += 1

        if "space" in console.keyspressed():
            if len(shoots) == 0:
                shoots.append((x, y))

        draw_ship(x, y, buffer)

        for i, (_x, _y, speed, color, c) in enumerate(asteroids):
            buffer.set_foreign_color(color)
            buffer.putchxy(_x, _y, c)
            buffer.resetall()

            _y += speed

            if _y > rows:
                _x = random.randint(0, columns)
                _y = 0

            if _x in range(x, x + 3) and _y in range(y, y + 3):
                if c == '.':
                    score += 1
                else:
                    life -= 5

                asteroids.remove(asteroids[i])
                asteroids.append(random_asteroid(_y=(0, 0)))
            else:
                asteroids[i] = _x, _y, speed, color, c

        for i, (_x, _y) in enumerate(shoots):
            _y -= 1
            buffer.set_foreign_color((0, 255, 0))
            buffer.putchxy(_x, _y, '0')
            buffer.resetall()

            if _y < 0:
                shoots.remove(shoots[i])
            else:
                shoots[i] = _x, _y

        for i, (_x, _y) in enumerate(shoots):
            for j, (_xx, _yy, speed, color, c) in enumerate(asteroids):
                if _x == _xx and _y == _yy:
                    asteroids.remove(asteroids[j])
                    score += 1

        buffer.bold(True)
        buffer.gotoxy(1, 1)
        buffer.print(f"life: {life}")
        buffer.resetall()
        buffer.gotoxy(1, 2)
        buffer.print(f"score: {score}")
        buffer.resetall()
    else:
        _msg = "You lost!"
        buffer.bold(True)
        buffer.cputsxy(40 - (len(_msg) // 2), 15, _msg)

        buffer.resetall()

        _msg = "Press SPACE for play again"
        buffer.set_foreign_color((255, 0, 0))
        buffer.cputsxy(40 - (len(_msg) // 2), 16, _msg)

        buffer.resetall()

        if "space" in console.keyspressed():
            life = 100


if __name__ == '__main__':
    console.set_title("Asteroids")
    console.set_font("ModernDOS8x16.ttf")
    console.set_target(loop)
    console.main_loop()
