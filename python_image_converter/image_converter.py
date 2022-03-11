from itertools import count
from PIL import Image, ImageColor
from os import listdir
from os.path import isfile, join

from matplotlib.colors import hex2color, rgb2hex

images_path = "./images"
images_bmp_path = "./images_bmp"
output_path = "./output"

# hex colors of black, white, gree, blue, red, yellow, and orange
palette = [0x000000, 0xFFFFFF, 0x00FF00, 0x0000FF, 0xFF0000, 0xFFFF00, 0xFF8000]

def convert_tuple_to_hex(color):
    color_norm = (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1.0)
    old_color_val = int(rgb2hex(color_norm)[1:], 16)
    return old_color_val

def find_closest_palette_color(old_color):
    """
    Find the closest color in the palette to the given color.
    """
    min_distance = None
    closest_color = None
    for color in palette:
        # normalize old color
        old_color_val = convert_tuple_to_hex(old_color)
        distance = abs(color - old_color_val)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

def hex_to_rgb(hex_color):
    string_val = str(hex(hex_color))[2:].zfill(6)
    return ImageColor.getcolor('#' + string_val, "RGB")

# Open all images and convert them to bmp
# for image_name in listdir(images_path):
#     if isfile(join(images_path, image_name)):
#         image = Image.open(join(images_path, image_name))
#         img_dithered = hd.ordered.bayer.bayer_dithering(image, palette, [256/4, 256/4, 256/4], order=8)
#         img_dithered.save(join(images_bmp_path, image_name.replace(".png", ".bmp")))

# print(image.size[0], image.size[1])

image = Image.open(join(images_path, "color_wheel.jpg"))
output = []

# duplicate image data
new_image = image.copy()

# read every pixel from a non-BMP file
for y in range(0, new_image.size[1] - 1):
    for x in range(1, new_image.size[0] - 1):
        # get pixel value
        pixel = new_image.getpixel((x, y))
        pixel_hex = convert_tuple_to_hex(pixel)

        new_pixel = find_closest_palette_color(pixel)
        new_image.putpixel((x, y), new_pixel)
        # quant_error = pixel_hex - new_pixel
        
        # adjacent_pixel = list(new_image.getpixel((x + 1, y)))
        # # adjacent_pixel[0] += int(quant_error * 7 / 16)
        # # adjacent_pixel[1] += int(quant_error * 7 / 16)
        # # adjacent_pixel[2] += int(quant_error * 7 / 16)
        # # new_image.putpixel((x + 1, y), tuple(adjacent_pixel))

        # adjacent_pixel = list(new_image.getpixel((x - 1, y + 1)))
        # # adjacent_pixel[0] += int(quant_error * 3 / 16)
        # # adjacent_pixel[1] += int(quant_error * 3 / 16)
        # # adjacent_pixel[2] += int(quant_error * 3 / 16)
        # # new_image.putpixel((x - 1, y + 1), tuple(adjacent_pixel))
        
        # adjacent_pixel = list(new_image.getpixel((x, y + 1)))
        # # adjacent_pixel[0] += int(quant_error * 5 / 16)
        # # adjacent_pixel[1] += int(quant_error * 5 / 16)
        # # adjacent_pixel[2] += int(quant_error * 5 / 16)
        # # new_image.putpixel((x, y + 1), tuple(adjacent_pixel))

        # adjacent_pixel = list(new_image.getpixel((x + 1, y + 1)))
        # # adjacent_pixel[0] += int(quant_error * 1 / 16)
        # # adjacent_pixel[1] += int(quant_error * 1 / 16)
        # # adjacent_pixel[2] += int(quant_error * 1 / 16)
        # # new_image.putpixel((x + 1, y + 1), tuple(adjacent_pixel))

# save image
new_image.save(join(output_path, "color_wheel_dithered.png"))

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
