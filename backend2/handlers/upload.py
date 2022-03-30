import json
import boto3
import base64
import math

s3 = boto3.client('s3')

# Upload image


def uploadImage(event, context):
    body = json.loads(event['body'])
    image64Data = body['image64Data']
    if image64Data:
        # get hash of image
        imageHash = hash(image64Data)

        # get image from base64
        image = base64.b64decode(image64Data)
        dithered_image = get_dithered_image(image)

        # upload image to S3
        s3.put_object(
            Bucket="image-data",
            Key=f'{str(imageHash)}/dithered_image.png',
            Body=dithered_image,
            ContentType='image/png'
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"hash": imageHash})
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "NO IMAGE"})
        }


# black, white, red, green, blue, yellow, orange
palette = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
           (0, 0, 255), (255, 255, 0), (255, 128, 0)]
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


def get_dithered_image(image):
    # read every pixel from a non-BMP file
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            # get pixel value
            old_pixel = image.getpixel((x, y))

            new_pixel = find_closest_palette_color(old_pixel)
            image.putpixel((x, y), new_pixel)

            quant_error = subtract_tuple(old_pixel, new_pixel)

            if x + 1 < image.size[0]:
                adjacent_pixel = list(image.getpixel((x + 1, y)))
                adjacent_pixel[0] += int(quant_error[0] * 7 / 16)
                adjacent_pixel[1] += int(quant_error[1] * 7 / 16)
                adjacent_pixel[2] += int(quant_error[2] * 7 / 16)
                image.putpixel((x + 1, y), tuple(adjacent_pixel))

            if x - 1 >= 0 and y + 1 < image.size[1]:
                adjacent_pixel = list(image.getpixel((x - 1, y + 1)))
                adjacent_pixel[0] += int(quant_error[0] * 3 / 16)
                adjacent_pixel[1] += int(quant_error[1] * 3 / 16)
                adjacent_pixel[2] += int(quant_error[2] * 3 / 16)
                image.putpixel((x - 1, y + 1), tuple(adjacent_pixel))

            if y + 1 < image.size[1]:
                adjacent_pixel = list(image.getpixel((x, y + 1)))
                adjacent_pixel[0] += int(quant_error[0] * 5 / 16)
                adjacent_pixel[1] += int(quant_error[1] * 5 / 16)
                adjacent_pixel[2] += int(quant_error[2] * 5 / 16)
                image.putpixel((x, y + 1), tuple(adjacent_pixel))

            if x + 1 < image.size[0] and y + 1 < image.size[1]:
                adjacent_pixel = list(image.getpixel((x + 1, y + 1)))
                adjacent_pixel[0] += int(quant_error[0] * 1 / 16)
                adjacent_pixel[1] += int(quant_error[1] * 1 / 16)
                adjacent_pixel[2] += int(quant_error[2] * 1 / 16)
                image.putpixel((x + 1, y + 1), tuple(adjacent_pixel))
    return image
