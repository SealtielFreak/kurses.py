import math

import numpy as np
import sdl2
import sdl2.sdlmixer as sdl2mixer

from kurses.resources.buzzer import Buzzer
from kurses.resources.mixer.effect import Effect
from kurses.resources.mixer.music import Music


class SDL2Effect(Effect):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.__sample = sdl2mixer.Mix_LoadWAV(filename.encode('utf-8'))

        if not self.__sample:
            raise RuntimeError(f"The file could not be loaded: {sdl2mixer.Mix_GetError().decode('utf-8')}")

        self.__channel = -1

    def __del__(self):
        if self.__sample:
            sdl2mixer.Mix_FreeChunk(self.__sample)

    def play(self, loops=0):
        self.__channel = sdl2mixer.Mix_PlayChannel(-1, self.__sample, loops)

    def volume(self, value=None):
        if value is None:
            return sdl2mixer.Mix_VolumeChunk(self.__sample, -1)

        return sdl2mixer.Mix_VolumeChunk(self.__sample, value)

    def stop(self):
        if self.__channel != -1:
            sdl2mixer.Mix_HaltChannel(self.__channel)


class SDL2Music(Music):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.__music = sdl2mixer.Mix_LoadMUS(filename.encode('utf-8'))

        if not self.__music:
            raise RuntimeError(f"The music could not be loaded: {sdl2mixer.Mix_GetError().decode('utf-8')}")

    def __del__(self):
        if self.__music:
            sdl2mixer.Mix_FreeMusic(self.__music)

    def play(self, loops=0):
        if sdl2mixer.Mix_PlayMusic(self.__music, loops) == -1:
            raise RuntimeError(f"Error playing music: {sdl2mixer.Mix_GetError().decode('utf-8')}")

    def loop(self, repeat=True):
        loops = -1 if repeat else 0
        self.play(loops)

    def fadeout(self, seconds):
        sdl2mixer.Mix_FadeOutMusic(math.ceil(seconds * 1000))

    def volume(self, value=None):
        if value is None:
            return sdl2mixer.Mix_VolumeMusic(-1)

        return sdl2mixer.Mix_VolumeMusic(int(value))

    def resume(self):
        sdl2mixer.Mix_ResumeMusic()

    def pause(self):
        sdl2mixer.Mix_PauseMusic()

    def stop(self):
        sdl2mixer.Mix_HaltMusic()


class SDL2Buzzer(Buzzer):
    def __init__(self, sample_rate=44100):
        self.__library = {}
        self.__looping_id = None
        self.__current_volume = 50

        self.sample_rate = sample_rate
        self.spec = sdl2.SDL_AudioSpec(
            freq=self.sample_rate,
            aformat=sdl2.AUDIO_S16SYS,
            channels=1,
            samples=2048
        )

        self.device_id = sdl2.SDL_OpenAudioDevice(None, 0, self.spec, None, 0)
        if self.device_id == 0:
            raise RuntimeError(f"The audio device could not be opened: {sdl2.SDL_GetError()}")

    def playing(self):
        return sdl2.SDL_GetQueuedAudioSize(self.device_id) > 0

    def update(self):
        if self.__looping_id is not None and not self.playing():
            self.play(self.__looping_id, volume=self.__current_volume, loop=True)

    def stop(self):
        self.__looping_id = None
        sdl2.SDL_ClearQueuedAudio(self.device_id)
        sdl2.SDL_PauseAudioDevice(self.device_id, 1)

    def record(self, track_id, notes):
        self.__library[track_id] = notes

    def play(self, track_id, volume=50, loop=None):
        if track_id not in self.__library:
            return

        self.__looping_id = track_id if loop else None
        self.__current_volume = volume

        track = self.__library[track_id]
        full_track_data = []

        for freq, duration_ms in track:
            actual_duration = min(duration_ms, 1000)
            num_samples = int(self.sample_rate * (actual_duration / 1000.0))

            if freq > 0:
                t = np.linspace(0, actual_duration / 1000.0, num_samples, False)
                wave = np.sign(np.sin(2 * np.pi * freq * t))
                vol_factor = volume / 100.0
                note_data = (wave * vol_factor * 16000).astype(np.int16)
                full_track_data.append(note_data)
            else:
                silence = np.zeros(num_samples, dtype=np.int16)
                full_track_data.append(silence)

        if full_track_data:
            final_buffer = np.concatenate(full_track_data).tobytes()
            sdl2.SDL_ClearQueuedAudio(self.device_id)
            sdl2.SDL_QueueAudio(self.device_id, final_buffer, len(final_buffer))
            sdl2.SDL_PauseAudioDevice(self.device_id, 0)

    def beep(self, frequency, duration_ms, volume=50):
        self.__looping_id = None

        actual_duration = min(duration_ms, 1000)
        num_samples = int(self.sample_rate * (actual_duration / 1000.0))

        t = np.linspace(0, actual_duration / 1000.0, num_samples, False)
        wave = np.sin(2 * np.pi * frequency * t)

        vol_factor = volume / 100.0
        audio_data = (wave * vol_factor * 32767).astype(np.int16)
        raw_data = audio_data.tobytes()

        sdl2.SDL_ClearQueuedAudio(self.device_id)
        sdl2.SDL_QueueAudio(self.device_id, raw_data, len(raw_data))
        sdl2.SDL_PauseAudioDevice(self.device_id, 0)

    def __del__(self):
        if hasattr(self, 'device_id') and self.device_id:
            sdl2.SDL_CloseAudioDevice(self.device_id)
