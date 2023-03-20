import dataclasses


@dataclasses.dataclass
class CharacterAttribute:
    code: chr = ''
    x: int = 0
    y: int = 0
    foreign: int = 0xFFFFFF
    background: int = 0
    style: int = 0x0

    def __eq__(self, other):
        return self.code == other.code and self.foreign == other.foreign and self.background == other.background and self.style == other.style

    def __hash__(self):
        return hash((self.code, self.foreign, self.background, self.style))

    def __bool__(self):
        return self == CharacterAttribute()
