from PIL import Image
from ColorFormats import rgb_to_hsv, hsv_to_rgb
import os

def create_single_color_image(color, size=(150, 150), filename='single_color_image.png'):
    """
    Create an image of a single color.

    Parameters:
    - color: tuple of RGB (e.g., (255, 0, 0)) or hex (e.g., "#FF0000") color code.
    - size: tuple of width and height (default is 150x150).
    - filename: name of the file to save the image (default is 'single_color_image.png').

    Returns:
    - None
    """
    # Convert hex color to RGB if needed
    if isinstance(color, str):
        if color.startswith('#'):
            color = color.lstrip('#')
            color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    # Create an image
    image = Image.new("RGB", size, color)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the image
    image.save(filename)
    print(f"Image saved as {filename}")



def rainbow():
    # Create a folder called 'folder' and save images inside it
    folder = 'rainbow'

    create_single_color_image((255, 0, 0), size=(150, 150), filename=f'{folder}/red_image.png')
    create_single_color_image((255, 165, 0), size=(150, 150), filename=f'{folder}/orange_image.png')
    create_single_color_image((255, 255, 0), size=(150, 150), filename=f'{folder}/yellow_image.png')
    create_single_color_image((0, 255, 0), size=(150, 150), filename=f'{folder}/green_image.png')
    create_single_color_image((0, 0, 255), size=(150, 150), filename=f'{folder}/blue_image.png')
    create_single_color_image((75, 0, 130), size=(150, 150), filename=f'{folder}/indigo_image.png')
    create_single_color_image((238, 130, 238), size=(150, 150), filename=f'{folder}/violet_image.png')

def add_tint(color, factor):
    """
    Add a tint to the given color by blending it with white.
    :param color: Tuple of (R, G, B) values.
    :param factor: Float in range [0, 1] where 0 is the original color and 1 is white.
    :return: Tuple of (R, G, B) values for the tinted color.
    """
    r, g, b = color
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return (r, g, b)

def add_shade(color, factor):
    """
    Add a shade to the given color by blending it with black.
    :param color: Tuple of (R, G, B) values.
    :param factor: Float in range [0, 1] where 0 is the original color and 1 is black.
    :return: Tuple of (R, G, B) values for the shaded color.
    """
    r, g, b = color
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return (r, g, b)

def generate_monochrome_scheme(color, num_tints=50, num_shades=50):
    """
    Generate a monochrome color scheme with tints and shades.
    :param color: Tuple of (R, G, B) values.
    :param num_tints: Number of tints to generate.
    :param num_shades: Number of shades to generate.
    :return: List of (R, G, B) values for the color scheme.
    """
    scheme = [color]
    for i in range(1, num_tints + 1):
        scheme.append(add_tint(color, i / (num_tints + 1)))
    for i in range(1, num_shades + 1):
        scheme.append(add_shade(color, i / (num_shades + 1)))
    return scheme

# original_color = (50, 80, 90)

def create_monochrome(original_color):  
    monochrome_scheme = generate_monochrome_scheme(original_color)
    counter = 1
    for color in monochrome_scheme:
        print(color)
        folder = 'monochrome'
        create_single_color_image(color, size=(150, 150), filename=f'{folder}/{counter}.png')
        counter+=1

#NOTE this complementary is for the rgb model, which means these are complementary colors 
# Red and Cyan
# Green and Magenta
# Blue and Yellow

# instead of the rgb complementary colors
# Red and Green
# Yellow and Purple
# Blue and Orange

def find_complementary_color(rgb_color):
    """
    Find the complementary color of the given RGB color.
    :param rgb_color: Tuple of (R, G, B) values.
    :return: Tuple of (R, G, B) values for the complementary color.
    """
    r, g, b = rgb_color
    complementary_color = (255 - r, 255 - g, 255 - b)
    return complementary_color

def create_complementary(original_color):
    complementary_color = find_complementary_color(original_color)
    complementary_colors_list = generate_monochrome_scheme(original_color)
    complementary_colors_list.extend(generate_monochrome_scheme(complementary_color))
    counter = 1
    for color in complementary_colors_list:
        print(color)
        folder = 'complementary'
        create_single_color_image(color, size=(150, 150), filename=f'{folder}/{counter}.png')
        counter+=1



def find_analogous_colors(rgb_color, num_colors=3, angle=30):
    """
    Find analogous colors for the given RGB color.
    :param rgb_color: Tuple of (R, G, B) values.
    :param num_colors: Number of analogous colors to generate (including the original color).
    :param angle: Angle (in degrees) to determine how far apart the analogous colors should be on the color wheel.
    :return: List of tuples, each tuple represents an analogous RGB color.
    """
    r, g, b = rgb_color
    analogous_colors = []
    for i in range(num_colors):
        hue_shift = angle * (i - (num_colors // 2))
        h, s, v = rgb_to_hsv(r, g, b)
        new_h = (h + hue_shift) % 360
        new_r, new_g, new_b = hsv_to_rgb(new_h, s, v)
        analogous_colors.append((new_r, new_g, new_b))
    return analogous_colors

def create_analogous(original_color):
    alist = find_analogous_colors(original_color)
    analogous_colors = []
    for items in alist:
        analogous_colors.extend(generate_monochrome_scheme(items, num_shades=10,num_tints=10))
    counter = 1
    for color in analogous_colors:
        print(color)
        folder = 'analogous'
        create_single_color_image(color, size=(150, 150), filename=f'{folder}/{counter}.png')
        counter+=1


def find_triadic_colors(rgb_color):
    """
    Find triadic colors for the given RGB color.
    :param rgb_color: Tuple of (R, G, B) values.
    :return: List of tuples, each tuple represents a triadic RGB color.
    """
    r, g, b = rgb_color
    triadic_colors = []

    # Calculate first triadic color (120 degrees apart)
    h1, s1, v1 = rgb_to_hsv(r, g, b)
    new_h1 = (h1 + 120) % 360
    new_r1, new_g1, new_b1 = hsv_to_rgb(new_h1, s1, v1)
    triadic_colors.append((new_r1, new_g1, new_b1))

    # Calculate second triadic color (240 degrees apart)
    h2, s2, v2 = rgb_to_hsv(r, g, b)
    new_h2 = (h2 + 240) % 360
    new_r2, new_g2, new_b2 = hsv_to_rgb(new_h2, s2, v2)
    triadic_colors.append((new_r2, new_g2, new_b2))

    return triadic_colors

def create_triadic(original_color):
    triadic_colors = find_triadic_colors(original_color)
    triadic_list = []
    for items in triadic_colors:
        triadic_list.extend(generate_monochrome_scheme(items, num_shades=10,num_tints=10))
    counter = 1
    for color in triadic_list:
        print(color)
        folder = 'triadic'
        create_single_color_image(color, size=(150, 150), filename=f'{folder}/{counter}.png')
        counter+=1

def is_warm_color(rgb_color):
    """
    Check if the given RGB color is a warm color.
    :param rgb_color: Tuple of (R, G, B) values.
    :return: True if the color is warm, False if it is cool.
    """
    r, g, b = rgb_color
    # Calculate a "warmth score" based on RGB values
    warmth_score = r - (g + b) / 2

    # Define a threshold to classify as warm or cool
    threshold = 20

    # Check if warmth score is above the threshold
    return warmth_score >= threshold

def is_cool_color(rgb_color):
    """
    Check if the given RGB color is a cool color.
    :param rgb_color: Tuple of (R, G, B) values.
    :return: True if the color is cool, False if it is warm.
    """
    return not is_warm_color(rgb_color)

