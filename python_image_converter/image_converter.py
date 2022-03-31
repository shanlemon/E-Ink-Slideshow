from itertools import count
from logging import PlaceHolder
from PIL import Image, ImageColor, ImageOps
from os import listdir
from os.path import isfile, join
import math
import base64

from matplotlib.colors import hex2color, rgb2hex

images_path = "./images"
images_bmp_path = "./images_bmp"
output_path = "./output"
image_output_dimensions = (600, 448)

image_name = "rog"

# black, white, red, green, blue, yellow, orange
palette = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 128, 0)]
palette_binary = ["0000", "0001", "0100", "0010", "0011", "0101", "0110"]

def subtract_tuple(tuple_a, tuple_b):
    return tuple(map(lambda i, j: i - j, tuple_a, tuple_b))

def find_closest_palette_color(color):
    min_distance = None
    closest_color = None
    for palette_color in palette:
        # keep first three values
        color = color[:3]

        distance = math.dist(color, palette_color)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_color = palette_color
    return closest_color

image = Image.open(join(images_path, image_name + ".png"))

# duplicate image data
new_image = ImageOps.fit(image, image_output_dimensions, method = 0,
                   bleed = 0.0, centering =(0.5, 0.5))

# read every pixel from a non-BMP file
for y in range(0, new_image.size[1]):
    for x in range(0, new_image.size[0]):
        # get pixel value
        old_pixel = new_image.getpixel((x, y))

        new_pixel = find_closest_palette_color(old_pixel)
        new_image.putpixel((x, y), new_pixel)

        quant_error = subtract_tuple(old_pixel, new_pixel)
        
        if x + 1 < new_image.size[0]:
            adjacent_pixel = list(new_image.getpixel((x + 1, y)))
            adjacent_pixel[0] += int(quant_error[0] * 7 / 16)
            adjacent_pixel[1] += int(quant_error[1] * 7 / 16)
            adjacent_pixel[2] += int(quant_error[2] * 7 / 16)
            new_image.putpixel((x + 1, y), tuple(adjacent_pixel))
        
        if x - 1 >= 0 and y + 1 < new_image.size[1]:
            adjacent_pixel = list(new_image.getpixel((x - 1, y + 1)))
            adjacent_pixel[0] += int(quant_error[0] * 3 / 16)
            adjacent_pixel[1] += int(quant_error[1] * 3 / 16)
            adjacent_pixel[2] += int(quant_error[2] * 3 / 16)
            new_image.putpixel((x - 1, y + 1), tuple(adjacent_pixel))
        
        if y + 1 < new_image.size[1]:
            adjacent_pixel = list(new_image.getpixel((x, y + 1)))
            adjacent_pixel[0] += int(quant_error[0] * 5 / 16)
            adjacent_pixel[1] += int(quant_error[1] * 5 / 16)
            adjacent_pixel[2] += int(quant_error[2] * 5 / 16)
            new_image.putpixel((x, y + 1), tuple(adjacent_pixel))

        if x + 1 < new_image.size[0] and y + 1 < new_image.size[1]:
            adjacent_pixel = list(new_image.getpixel((x + 1, y + 1)))
            adjacent_pixel[0] += int(quant_error[0] * 1 / 16)
            adjacent_pixel[1] += int(quant_error[1] * 1 / 16)
            adjacent_pixel[2] += int(quant_error[2] * 1 / 16)
            new_image.putpixel((x + 1, y + 1), tuple(adjacent_pixel))

# save image
new_image.save(join(output_path, image_name + "_dithered.png"))


output = []

def color_to_binary(color1):
    color_rgb = color1[:3]
    return palette_binary[palette.index(color_rgb)]

# read every pixel from BMP file
for i in range(0, new_image.size[1]):
    for j in range(0, new_image.size[0], 2):
        # get pixel value
        pixel1 = new_image.getpixel((j, i))
        pixel2 = new_image.getpixel((j+1, i))
        
        binary_1 = color_to_binary(pixel1)
        binary_2 = color_to_binary(pixel2)

        combined = binary_1 + binary_2
            
        hex_version = int(combined, 2)
        byte_version = hex_version.to_bytes(1, 'big')
        output.append(byte_version)


with open('output.txt', 'w') as f:
    f.write(base64.b64encode(b''.join(output)).decode("utf-8"))

