# Audio

`kurses.py` can play sound effects, music and simple synthesized beeps through
the SDL2 mixer backend.

## What you will learn

- How to enable sound with `sound_enabled=True`.
- How to load [`Effect`][kurses.backend.sdl2.resources.mixer.SDL2Effect] and
  [`Music`][kurses.backend.sdl2.resources.mixer.SDL2Music] objects.
- How to use the [`Buzzer`][kurses.resources.buzzer.Buzzer] to record and play
  tone tracks.

## Complete example

```python
from kurses import Effect, Music, VirtualTerminal

term = VirtualTerminal(
    font_filename="ModernDOS8x16.ttf",
    sound_enabled=True,
)
stream = term.stream
buzzer = term.buzzer

# Record a short melody track
buzzer.record(0, [(440, 200), (493, 200), (523, 200), (587, 400)])

# Load sound effect and music
laser = Effect(filename="laser.mp3")
laser.volume(10)

music = Music(filename="win95.mp3")
music.volume(15)
music.play(2)
music.fadeout(5)


def loop():
    stream.resetall()
    stream.gotoxy(0, 0)
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))
    stream.print("Sounds")

    stream.gotoxy(5, 1)
    stream.italic(True)
    stream.print("in Kurses!")

    keys = term.keyspressed()

    if "space" in keys:
        laser.play(2)

    if "w" in keys:
        buzzer.play(0, 25)

    if "s" in keys:
        buzzer.beep(440, 25, 25)


term.set_target(loop)
term.main_loop()
```

## Breaking it down

### Enable sound

```python
term = VirtualTerminal(font_filename="ModernDOS8x16.ttf", sound_enabled=True)
```

Without `sound_enabled=True`, the audio system is not initialized.

### Sound effects

```python
laser = Effect(filename="laser.mp3")
laser.volume(10)
laser.play(2)
```

[`Effect`][kurses.backend.sdl2.resources.mixer.SDL2Effect] plays short sounds.
`play(loops)` receives the number of extra loops (`2` means three total plays).

### Music

```python
music = Music(filename="win95.mp3")
music.play(2)
music.fadeout(5)
```

[`Music`][kurses.backend.sdl2.resources.mixer.SDL2Music] streams larger files.
`fadeout(seconds)` fades the music out over the given time.

### Buzzer

```python
buzzer.record(0, [(440, 200), (493, 200), (523, 200), (587, 400)])
buzzer.play(0, 25)
```

`Buzzer.record(track_id, notes)` stores a list of `(frequency, duration_ms)`
pairs. `Buzzer.play(track_id, volume)` plays them back.

## Try it

Replace the bundled `laser.mp3` and `win95.mp3` with your own files.

## Next tutorial

Draw 2D primitives in [Bitmap Graphics](bitmap-graphics.md).
