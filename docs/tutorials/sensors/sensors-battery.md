# Sensors and Battery

`kurses.py` exposes SDL2 power and sensor information, which is useful on
laptops and mobile platforms.

## What you will learn

- How to read battery status with `battery()`.
- How to read gyroscope and accelerometer data with
  [`gyroscope()`][kurses.term.VirtualTerminal.gyroscope] and
  [`accelerometer()`][kurses.term.VirtualTerminal.accelerometer].

## Battery example

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    bat_status, bat_value = term.battery()

    stream.resetall()

    stream.gotoxy(0, 0)
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))
    stream.print(f"Battery status: {bat_status}")

    stream.gotoxy(0, 1)
    stream.italic(True)
    stream.print(f"Battery value: {bat_value}%")


term.title = "Battery demo"
term.set_target(loop)
term.main_loop()
```

## Sensors example

```python
from kurses import VirtualTerminal

term = VirtualTerminal(font_filename="ModernDOS8x16.ttf")
stream = term.stream


def loop():
    gyro = term.gyroscope()
    acce = term.accelerometer()

    stream.resetall()
    stream.set_background_color((255, 255, 255))
    stream.set_foreign_color((0, 0, 0))

    stream.gotoxy(0, 0)
    stream.print(f"Gyroscope: {gyro}")

    stream.gotoxy(0, 1)
    stream.print(f"Accelerometer: {acce}")


term.title = "Sensors demo (Gyroscope and accelerometer)"
term.set_target(loop)
term.main_loop()
```

## Breaking it down

### Battery status

```python
status, value = term.battery()
```

`battery()` returns a [`BatteryStatus`][kurses.interface.battery.BatteryStatus]
enum value and an integer percentage.

### Sensors

```python
available, (x, y, z) = term.gyroscope()
```

[`gyroscope()`][kurses.term.VirtualTerminal.gyroscope] and
[`accelerometer()`][kurses.term.VirtualTerminal.accelerometer] return a tuple
`(available, (x, y, z))`. If no sensor is detected, `available` is `False`.

## Try it

Combine the two demos into a single status panel.

## Next tutorial

Handle touchscreens in [Touch Input](touch-input.md).
