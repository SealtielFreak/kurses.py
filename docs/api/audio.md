# Audio

Audio is handled through SDL2 mixer. The public abstractions live in
`kurses.resources`, while the SDL2 implementation lives in
`kurses.backend.sdl2.resources`.

## kurses.resources.mixer

::: kurses.resources.mixer
    options:
      members:
        - AudioSystem
        - Sound
        - Effect
        - Music

## kurses.resources.mixer.sound

::: kurses.resources.mixer.sound
    options:
      members:
        - Sound

## kurses.resources.buzzer

::: kurses.resources.buzzer
    options:
      members:
        - Buzzer

## kurses.backend.sdl2.resources.mixer

::: kurses.backend.sdl2.resources.mixer
    options:
      members:
        - SDL2AudioSystem
        - SDL2Buzzer
        - SDL2Effect
        - SDL2Music
