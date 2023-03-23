

def get_true_colors():
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                yield r, g, b


def get_8bit_colors():
    for r in range(0, 256, 36):
        for g in range(0, 256, 36):
            for b in range(0, 256, 85):
                yield r, g, b


def get_2bit_colors():
    for r in (0, 85, 170, 255):
        for g in (0, 85, 170, 255):
            for b in (0, 85, 170, 255):
                yield r, g, b


def get_1bit_colors():
    for r in range(0, 256, 255):
        for g in range(0, 256, 255):
            for b in range(0, 256, 255):
                yield r, g, b


def rgb_to_bit_depth(rgb, bit_depth):
    factor = 256 // bit_depth
    r, g, b = rgb

    r = r // factor * factor
    g = g // factor * factor
    b = b // factor * factor

    return (r << 16) + (g << 8)