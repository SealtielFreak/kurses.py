import random
import sys
import collections
import threading
import time

import sdl2
import sdl2.ext


class Character:
    def __init__(self, c):
        self.__c = c

    @property
    def char(self):
        return self.__c


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class MainThreadPipe(metaclass=SingletonMeta):
    def __init__(self):
        self.__queue = collections.deque()
        self.__close = False

    @property
    def close(self):
        return self.__close

    def finished(self):
        self.__close = True

    @property
    def empty(self):
        return len(self.__queue) == 0

    def push(self, c):
        self.__queue.append(c)

    def pop(self):
        return self.__queue.popleft()


def main_thread_loop():
    sdl2.ext.init()
    main_pipe = MainThreadPipe()

    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()

    running = True

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

        if not main_pipe.empty:
            print(f"Pop message: {main_pipe.pop()}")

        if main_pipe.close:
            break

        window.refresh()

    return 0


def queue_thread():
    main_pipe = MainThreadPipe()

    for i in range(10):
        main_pipe.push(i)

        time.sleep(1)

    print("Queue thread finished")

    main_pipe.finished()


if __name__ == "__main__":
    thread = threading.Thread(target=queue_thread)
    thread.start()
    main_thread_loop()
    thread.join()
