import dataclasses


@dataclasses.dataclass
class CharacterValue:
    code: chr = ''
    fg: int = 0xFFFFFF
    bg: int = 0
    style: int = 0x0
    x: int = 0
    y: int = 0

    def __eq__(self, other):
        return self.code == other.code and self.fg == other.fg and self.bg == other.bg and self.style == other.style

    def __hash__(self):
        return hash((self.code, self.fg, self.bg, self.style))

    def __bool__(self):
        return self == CharacterValue()
