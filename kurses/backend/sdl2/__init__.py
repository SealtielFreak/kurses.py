import ctypes
import math
import typing

import sdl2
import sdl2.sdlttf

import kurses.backend.sdl2.font_resources
import kurses.backend.sdl2.interface.joystick
import kurses.backend.sdl2.texture_surface
import kurses.colors
import kurses.events
import kurses.stream
import kurses.term
from kurses.backend.sdl2.resources import SDL2AudioSystem
from kurses.backend.sdl2.resources.mixer import SDL2Buzzer
from kurses.interface.battery import BatteryType, BatteryStatus
from kurses.interface.sensors import AccelerometerType, GyroscopeType
from kurses.interface.touch import TouchType
from kurses.resources.buzzer import Buzzer
from kurses.stream import StreamBuffer


def chr_format_key_sdl2(s):
    return s.decode().lower()


class SDL2VirtualTerminal(kurses.term.VirtualTerminal):
    __DEFAULT_WINDOW_POSITION = sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED

    __ALL_NAME_CLICK_STATE: typing.List[typing.List[str]] = [
        [],
        ['left'],
        ['middle'],
        ['left', 'middle'],
        ['right'],
        ['left', 'right'],
        ['right', 'middle'],
        ['left', 'right', 'middle']
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if sdl2.SDL_WasInit(sdl2.SDL_INIT_EVERYTHING) == 0:
            sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        if sdl2.sdlttf.TTF_WasInit() == 0:
            sdl2.sdlttf.TTF_Init()

        width, height = kwargs.get("size", (640, 480))
        position_x, position_y = self.__DEFAULT_WINDOW_POSITION
        self.__c_window = sdl2.SDL_CreateWindow(
            kwargs.get("title", "Virtual terminal").encode(),
            position_x,
            position_y,
            width,
            height,
            sdl2.SDL_WINDOW_SHOWN
        )

        self.__c_renderer = sdl2.SDL_CreateRenderer(
            self.window,
            -1,
            [sdl2.SDL_RENDERER_ACCELERATED, sdl2.SDL_RENDERER_SOFTWARE][self.type_rendering.value]
        )

        self.__target = kurses.events.empty_target
        self.__runtime_class = None
        self.__runtime = kurses.events.EmptyTargetRuntime()

        self.__font = kurses.backend.FontResources(self._font_filename)
        self.__textures_font = kurses.backend.TextureSurface(self.__font, self.streams)
        self.__bitmap = kurses.backend.BitmapSurface((width, height), self.graphics) if self.bitmap_enabled else None
        self.__joystick = kurses.backend.JoystickInterface()
        self.__mouse = [], (0, 0), (0, 0)

        self.__current_resizable_window = kwargs.get("resizable_window", True)
        self.resizable_window = self.__current_resizable_window

        if self.sound_enabled:
            self.__system_sound = SDL2AudioSystem()

        self.__buzzer = SDL2Buzzer()

        self.__c_sensors = {}
        self.__num_sensors = 0
        self.__gyroscope = False, (0, 0, 0)
        self.__accelerometer = False, (0, 0, 0)

        self.__c_active_fingers = {}

    def __del__(self):
        for s_id in self.__c_sensors:
            sdl2.SDL_SensorClose(self.__c_sensors[s_id]["handle"])

        if self.__c_renderer is not None:
            sdl2.SDL_DestroyRenderer(self.__c_renderer)

        if self.__c_window is not None:
            sdl2.SDL_DestroyWindow(self.__c_window)

    @property
    def buzzer(self) -> Buzzer:
        return self.__buzzer

    @property
    def title(self):
        return sdl2.SDL_GetWindowTitle(self.window)

    @title.setter
    def title(self, _str: str):
        sdl2.SDL_SetWindowTitle(self.window, _str.encode())

    @property
    def size(self) -> typing.Tuple[int, int]:
        w, h = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GetWindowSize(self.window, ctypes.byref(w), ctypes.byref(h))
        return w.value, h.value

    @property
    def resizable_window(self) -> bool:
        return self.__current_resizable_window

    @resizable_window.setter
    def resizable_window(self, resizable: bool):
        self.__current_resizable_window = resizable
        sdl2.SDL_SetWindowResizable(
            self.__c_window,
            self.__current_resizable_window
        )

    def set_target(self, target: typing.Callable[[], None]):
        self.__target = target

    def set_runtime(self, target: typing.Type[kurses.events.EventTargetRuntime]):
        self.__runtime_class = target

    def main_loop(self):
        if self.__runtime_class is not None:
            self.__runtime = self.__runtime_class()

        self.__runtime.load()

        if self.__bitmap:
            self.__bitmap.create(self.surface)

        self.__joystick.open()

        self.__num_sensors = sdl2.SDL_NumSensors()

        for i in range(self.__num_sensors):
            sensor_type = sdl2.SDL_SensorGetDeviceType(i)
            sensor_name = sdl2.SDL_SensorGetDeviceName(i).decode('utf-8')
            sensor_handle = sdl2.SDL_SensorOpen(i)

            if sensor_handle:
                sensor_id = sdl2.SDL_SensorGetInstanceID(sensor_handle)

                self.__c_sensors[sensor_id] = {
                    "name": sensor_name,
                    "type": sensor_type,
                    "handle": sensor_handle
                }

        while self.running:
            event = sdl2.SDL_Event()

            while sdl2.SDL_PollEvent(ctypes.byref(event)):
                self.push_events(event)

            self.__runtime.joystick(self.__joystick.inputs)

            if self.running:
                self.__runtime.update(self.dt)
                self.__target()

            self.clean()
            self.__runtime.draw()
            self.draw()

    def keyspressed(self) -> typing.List[str]:
        pressed_keys = []
        keyboard_state = sdl2.SDL_GetKeyboardState(None)

        for key_code in range(sdl2.SDL_NUM_SCANCODES):
            if keyboard_state[key_code] == 1:
                pressed_keys.append(chr_format_key_sdl2(sdl2.SDL_GetScancodeName(key_code)))

        return pressed_keys

    def joystick(self):
        return self.__joystick.inputs

    def mouse(self):
        return self.__mouse

    @property
    def window(self) -> sdl2.SDL_Window:
        return self.__c_window

    @property
    def surface(self) -> sdl2.SDL_Renderer:
        return self.__c_renderer

    def push_events(self, event: sdl2.SDL_Event):
        width, height = self.size
        rows, cols = self.stream.shape

        get_key_from_event = lambda e: chr_format_key_sdl2(sdl2.SDL_GetKeyName(e.key.keysym.sym))

        if event.type == sdl2.SDL_QUIT:
            self.quit()
            self.__runtime.exit()
        elif event.type == sdl2.SDL_WINDOWEVENT:
            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                width, height = event.window.data1, event.window.data2
                w, h = self.__font.size

                sdl2.SDL_SetWindowSize(self.window, width, height)

                self.__runtime.resize(self.resizable)

                if self.resizable:
                    for stream in self.streams:
                        if isinstance(stream, StreamBuffer):
                            stream.resize(width // w, height // h)

                    if self.__bitmap:
                        self.__bitmap.resize(width, height)

                self.__runtime.resize(self.resizable)
            elif event.window.event == sdl2.SDL_WINDOWEVENT_MINIMIZED:
                self.__runtime.minimized()
            elif event.window.event == sdl2.SDL_WINDOWEVENT_SHOWN:
                self.__runtime.showed()
            elif event.window.event == sdl2.SDL_WINDOWEVENT_EXPOSED:
                self.__runtime.exposed()
            elif event.window.event == sdl2.SDL_WINDOWEVENT_RESTORED:
                self.__runtime.restored()
        elif event.type == sdl2.SDL_KEYDOWN:
            self.__runtime.key_down(get_key_from_event(event))
        elif event.type == sdl2.SDL_KEYUP:
            self.__runtime.key_up(get_key_from_event(event))
        elif event.type == sdl2.SDL_MOUSEWHEEL:
            self.__runtime.scroll(event.wheel.y)
        elif event.type == sdl2.SDL_MOUSEMOTION:
            motion = event.motion

            x, y = motion.x, motion.y
            x, y = (math.ceil((x / width) * cols), math.ceil((y / height) * rows))

            state = self.__ALL_NAME_CLICK_STATE[motion.state]

            self.__mouse = state, (x, y), (motion.x, motion.y)
            self.__runtime.mouse(state, (x, y), (motion.x, motion.y))
        elif event.type == sdl2.SDL_SENSORUPDATE:
            sensor_id = event.sensor.which

            if sensor_id in self.__c_sensors:
                data = event.sensor.data
                s_type = self.__c_sensors[sensor_id]["type"]

                if s_type == sdl2.SDL_SENSOR_ACCEL:
                    self.__accelerometer = True, data
                elif s_type == sdl2.SDL_SENSOR_GYRO:
                    self.__gyroscope = True, data
        elif event.type == sdl2.SDL_FINGERDOWN:
            fid = event.tfinger.fingerId

            self.__c_active_fingers[fid] = (event.tfinger.x, event.tfinger.y)
        elif event.type == sdl2.SDL_FINGERMOTION:
            fid = event.tfinger.fingerId

            if fid in self.__c_active_fingers:
                self.__c_active_fingers[fid] = (event.tfinger.x, event.tfinger.y)

        elif event.type == sdl2.SDL_FINGERUP:
            fid = event.tfinger.fingerId

            if fid in self.__c_active_fingers:
                del self.__c_active_fingers[fid]

    def present(self):
        def _render_textures_font():
            self.__textures_font.present(self.surface)
            sdl2.SDL_RenderCopy(self.surface, self.__textures_font.current, None, None)

        def _render_bitmap():
            if self.__bitmap:
                self.__bitmap.present(self.surface)
                sdl2.SDL_RenderCopy(self.surface, self.__bitmap.current, None, None)

        render_order = [_render_textures_font, _render_bitmap]

        for render_runtime in render_order:
            render_runtime()

    def quit(self):
        self.running = False

    def draw(self):
        self.present()
        sdl2.SDL_RenderPresent(self.surface)

    def clean(self):
        sdl2.SDL_RenderClear(self.surface)
        self.__textures_font.clear(self.surface)

    def purge(self):
        if self.__bitmap:
            self.__bitmap.clear(self.surface)

    def gyroscope(self) -> GyroscopeType:
        return self.__gyroscope

    def accelerometer(self) -> AccelerometerType:
        return self.__accelerometer

    def touch(self) -> typing.List[TouchType]:
        def _read_fingers():
            for fid, (x, y) in self.__c_active_fingers.items():
                yield fid, (x, y)

        return list(*_read_fingers())

    def battery(self) -> BatteryType:
        secs = ctypes.c_int(0)
        pct = ctypes.c_int(0)

        status = sdl2.SDL_GetPowerInfo(ctypes.byref(secs), ctypes.byref(pct))

        if status == sdl2.SDL_POWERSTATE_NO_BATTERY:
            return BatteryStatus.NO_BATTERY, 0
        elif status == sdl2.SDL_POWERSTATE_ON_BATTERY:
            return BatteryStatus.ON_BATTERY, 0
        elif status == sdl2.SDL_POWERSTATE_CHARGING:
            return BatteryStatus.CHARGING, 0

        return BatteryStatus.UNKNOWN, 0
