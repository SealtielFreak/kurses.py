import enum
import typing


class BatteryStatus(enum.Enum):
    UNKNOWN = 0
    NO_BATTERY = 1
    ON_BATTERY = 2
    CHARGING = 3


BatteryType = typing.Tuple[BatteryStatus, int]
