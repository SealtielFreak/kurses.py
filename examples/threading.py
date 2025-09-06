import random
import time

import kurses.stream
from kurses import VirtualTerminal, StreamBuffer
from kurses.font_resources import QualityFont


console = VirtualTerminal(font_filename="ModernDOS8x16.ttf", quality=QualityFont.LCD)

main_buffer = console.stream

score_buffer = StreamBuffer(40, 15, sx=2, sy=2, type_cursor=kurses.stream.TypeCursor.RECT)
score_buffer.x = 0
score_buffer.y = 0
score_buffer.type_cursor = kurses.stream.TypeCursor.EMPTY


x_ship, y_ship = random.randint(0, 70), random.randint(0, 30)

life, score = 100, 0
shoots = []

def my_thread(buff):
    while True:
        print("Hello world")
        time.sleep(1)

        # raise Exception("Error raise!")

console.title = "Threading Demo"
console.set_thread_target(my_thread)
console.main_loop()
