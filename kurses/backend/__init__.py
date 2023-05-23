# So, I need work her

try:
    import sdl2
    from kurses.backend.sdl2 import SDL2VirtualTerminal

    VirtualTerminal = SDL2VirtualTerminal

except ImportError:
    try:
        raise ImportError("The module for Pygame has not been implemented yet.")
    except ImportError:
        raise ImportError("You need install pySDL2 for this module work!")

__all__ = ["VirtualTerminal"]
