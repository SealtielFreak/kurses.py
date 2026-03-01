import sdl2
import sdl2.sdlmixer as sdl2mixer

from kurses.resources.mixer import AudioSystem


class SDL2AudioSystem(AudioSystem):
    def __init__(self, frequency: int = 44100, format: int = sdl2mixer.MIX_DEFAULT_FORMAT, channels: int = 2):
        super().__init__(frequency, format, channels)

        if sdl2mixer.Mix_OpenAudio(frequency, format, channels, 2048) < 0:
            raise RuntimeError(f"The audio service could not be started: {sdl2mixer.Mix_GetError().decode('utf-8')}")

    def init(self):
        pass

    def enabled(self):
        pass
