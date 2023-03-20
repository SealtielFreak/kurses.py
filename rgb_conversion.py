def rgb_to_bit_depth(rgb, bit_depth):
  factor = 256 // bit_depth
  r, g, b = rgb

  r = r // factor * factor
  g = g // factor * factor
  b = b // factor * factor

  return (r << 16) + (g << 8)


if __name__ == "__main__":
    all_colors = set()

    for r in range(255):
        for g in range(255):
            for b in range(255):
                all_colors.add(rgb_to_bit_depth((r, g, b), 4))

                print(all_colors)
