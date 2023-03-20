try:
    import sdl2
    from pyrlkit.backend.sdl2 import SDL2VirtualConsole as Console

except ImportError as e:
    import pygame
    from pyrlkit.backend.pygame import PygameVirtualConsole as Console

__all__ = ["Console"]
