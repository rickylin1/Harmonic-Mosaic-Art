# hexadecimal is base 16 
# we use the following formula
#rgb ranges from (0,255) where (0,0,0) is black and (255,255,255) is white
# R/16 = x + y/16
# G/16 = x' + y'/16
# B/16 = x" + y"/16
#where x is a whole number and y is the remainder of the respective rgb value divided by 16
#then we can represent a hexadecimal such as 50068F which has 6 digits
#the numbers go from 0 - 9, then A - F for 10 - 15 

hex_colors_string = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11,
                  'C': 12, 'D': 13, 'E': 14, 'F': 15}

hex_colors = { 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F' }
    
def rgb_to_hex(r, g, b):
    r1, r2= r//16, int((r/16 - r//16) * 16)
    g1, g2= g//16, int((g/16 - g//16) * 16)
    b1, b2= b//16, int((b/16 - b//16) * 16)

    r1 = hex_colors[r1]
    g1 = hex_colors[g1]
    b1 = hex_colors[b1]
    r2 = hex_colors[r2]
    g2 = hex_colors[g2]
    b2 = hex_colors[b2]
   

    hex = str(r1) + str(r2) + str(g1) + str(g2) + str(b1) + str(b2)
    return hex

def hex_to_rgb(hex):
    l, r = 0, 1
    rgb = []
    for i in range(3):
        convert = hex_colors_string[hex[l]] * 16 + hex_colors_string[hex[r]]
        rgb.append(convert)
        l += 2
        r += 2
    return rgb

def rgb_to_cymk(r,g,b):
    white = max(r/255, g/255,b/255)
    cyan = (white - (r/255))/white
    magenta = (white - (g/255))/white
    yellow = (white - (b/255))/white
    black = 1 - white

def rgb_to_hsv(r, g, b):
    """
    Convert RGB to HSV (Hue, Saturation, Value/Brightness).
    :param r: Red value (0-255).
    :param g: Green value (0-255).
    :param b: Blue value (0-255).
    :return: Tuple of (H, S, V) where H is in range [0, 360], S and V are in range [0, 1].
    """
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    delta = max_rgb - min_rgb

    v = max_rgb / 255.0

    if max_rgb != 0:
        s = delta / max_rgb
    else:
        s = 0

    if delta == 0:
        h = 0
    elif r == max_rgb:
        h = (g - b) / delta
    elif g == max_rgb:
        h = 2 + (b - r) / delta
    else:
        h = 4 + (r - g) / delta

    h *= 60
    if h < 0:
        h += 360

    return h, s, v

def hsv_to_rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value/Brightness) to RGB.
    :param h: Hue value in degrees (0-360).
    :param s: Saturation value (0-1).
    :param v: Value/Brightness value (0-1).
    :return: Tuple of (R, G, B) where each value is in range [0, 255].
    """
    h /= 60
    i = int(h)
    f = h - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return int(r * 255), int(g * 255), int(b * 255)


