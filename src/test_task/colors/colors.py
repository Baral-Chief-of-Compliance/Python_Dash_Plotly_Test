def make_color_lighter(hex_str):

    hex_str = hex_str[1:]
    rgb = [int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)]

    for index, color in enumerate(rgb):
        if 255 - color > 150:
            rgb[index] = color + 150
            
        else:
            rgb[index] = 255


    hex_str = f'#{rgb[0]:x}{rgb[1]:x}{rgb[2]:x}'


    return hex_str