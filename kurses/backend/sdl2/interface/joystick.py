import sdl2

from kurses.interface.joystick import JoystickInterface


class SDL2JoystickInterface(JoystickInterface):
    __DEFAULT_VALUE_NORMALIZE = 32767.0

    __MAPPING_KEYS = {
        sdl2.SDL_CONTROLLER_BUTTON_A: "A",
        sdl2.SDL_CONTROLLER_BUTTON_B: "B",
        sdl2.SDL_CONTROLLER_BUTTON_X: "X",
        sdl2.SDL_CONTROLLER_BUTTON_Y: "Y",
        sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP: "UP",
        sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN: "DOWN",
        sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT: "LEFT",
        sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT: "RIGHT",
        sdl2.SDL_CONTROLLER_BUTTON_START: "START",
        sdl2.SDL_CONTROLLER_BUTTON_BACK: "BACK",
    }

    def __init__(self):
        self.__c_controllers = []

    def __del__(self):
        self.close()

    def open(self):
        n_joystick = sdl2.SDL_NumJoysticks()

        for i in range(n_joystick):
            if not sdl2.SDL_IsGameController(i):
                continue

            controller = sdl2.SDL_GameControllerOpen(i)

            if not controller:
                continue

            self.__c_controllers.append(controller)

    def update(self):
        self.close()
        self.open()

    def close(self):
        for controller in self.__c_controllers:
            sdl2.SDL_GameControllerClose(controller)

        self.__c_controllers.clear()

    @property
    def inputs(self):
        inputs = []

        for controller in self.__c_controllers:
            def get_axis(axis_id):
                return sdl2.SDL_GameControllerGetAxis(controller,
                                                      axis_id) / SDL2JoystickInterface.__DEFAULT_VALUE_NORMALIZE

            def get_trigger(axis_id):
                return sdl2.SDL_GameControllerGetAxis(controller,
                                                      axis_id) / SDL2JoystickInterface.__DEFAULT_VALUE_NORMALIZE

            buttons_set = set()

            for btn_id, name in SDL2JoystickInterface.__MAPPING_KEYS.items():
                if sdl2.SDL_GameControllerGetButton(controller, btn_id):
                    buttons_set.add(name)

            joystick = (
                sdl2.SDL_GameControllerName(controller).decode('utf-8'),
                buttons_set,
                (
                    (
                        'left',
                        bool(sdl2.SDL_GameControllerGetButton(controller, sdl2.SDL_CONTROLLER_BUTTON_LEFTSTICK)),
                        get_axis(sdl2.SDL_CONTROLLER_AXIS_LEFTX),
                        get_axis(sdl2.SDL_CONTROLLER_AXIS_LEFTY)
                    ),
                    (
                        'right',
                        bool(sdl2.SDL_GameControllerGetButton(controller, sdl2.SDL_CONTROLLER_BUTTON_RIGHTSTICK)),
                        get_axis(sdl2.SDL_CONTROLLER_AXIS_RIGHTX),
                        get_axis(sdl2.SDL_CONTROLLER_AXIS_RIGHTY)
                    ),
                ),
                (
                    (
                        'left',
                        bool(sdl2.SDL_GameControllerGetButton(controller, sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER)),
                        get_trigger(sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT),
                    ),
                    (
                        'right',
                        bool(sdl2.SDL_GameControllerGetButton(controller, sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER)),
                        get_trigger(sdl2.SDL_CONTROLLER_AXIS_TRIGGERRIGHT),
                    ),
                )
            )

            inputs.append(joystick)

        return inputs
