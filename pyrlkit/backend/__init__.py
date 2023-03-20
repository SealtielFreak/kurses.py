try:
    import pygame
    from pyrlkit.backend.pygame import PygameVirtualConsole as Console

except ImportError as e:
    import pysdl2
    from pyrlkit.backend.sdl2 import SDL2VirtualConsole as Console

__all__ = ["Console"]
