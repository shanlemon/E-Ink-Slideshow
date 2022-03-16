from itertools import count
from logging import PlaceHolder
from PIL import Image, ImageColor, ImageOps
from os import listdir
from os.path import isfile, join
import math

from matplotlib.colors import hex2color, rgb2hex

images_path = "./images"
images_bmp_path = "./images_bmp"
output_path = "./output"
image_output_dimensions = (600, 448)

image_name = "outdoors"

# black, white, red, green, blue, yellow, orange
palette = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 128, 0)]

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

image = Image.open(join(images_path, image_name + ".jpg"))

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


# output = []

# read every pixel from BMP file
# for i in range(0, image.size[1], 2):
#     for j in range(0, image.size[0]):
#         # get pixel value
#         pixel1 = image.getpixel((j, i))
#         pixel2 = image.getpixel((j, i+1))
#         binary_1 = "{0:b}".format(pixel1).zfill(4)
#         binary_2 = "{0:b}".format(pixel2).zfill(4)

#         combined = binary_1 + binary_2

#         if (len(binary_1) != 4):
#             print(binary_1)
            
#         hex_version = hex(int(combined, 2))
#         output.append(hex_version)

# print(output)
# print(len(output))

# # save print(output) to a file
# counter = 0
# total_lines = 0
# with open('output.txt', 'w') as f:
#     f.write('const unsigned char image[] = {')
#     for item in output:
#         f.write("%s, " % item)
#         counter += 1
#         if counter == 16:
#             f.write('\n')
#             total_lines += 1
#             counter = 0

#     f.write('};')

# print("wrote " + str(total_lines) + " lines")
