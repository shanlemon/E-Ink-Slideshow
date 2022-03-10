from itertools import count
from PIL import Image
image = Image.open('colors.bmp')

print(image.size[0], image.size[1])

output = []

# # read every pixel
for i in range(0, image.size[1], 2):
    for j in range(0, image.size[0]):
        # get pixel value
        pixel1 = image.getpixel((j, i))
        pixel2 = image.getpixel((j, i+1))
        binary_1 = "{0:b}".format(pixel1).zfill(4)
        binary_2 = "{0:b}".format(pixel2).zfill(4)


        combined = binary_1 + binary_2

        if (len(binary_1) != 4):
            print(binary_1)
            
        hex_version = hex(int(combined, 2))
        output.append(hex_version)

print(len(output))

# save print(output) to a file
counter = 0
total_lines = 0
with open('output.txt', 'w') as f:
    f.write('const unsigned char image[] = {')
    for item in output:
        f.write("%s, " % item)
        counter += 1
        if counter == 16:
            f.write('\n')
            total_lines += 1
            counter = 0

    f.write('};')

print("wrote " + str(total_lines) + " lines")
