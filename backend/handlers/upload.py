import json
import boto3
import base64
import math

s3 = boto3.client('s3')

# Upload image
def uploadImage(event, context):
    body = json.loads(event['body'])
    image64Data = body['image64Data']
    image64Data = body['rawData']

    if image64Data:
        # get hash of image
        imageHash = hash(image64Data)

        # get image from base64
        image = base64.b64decode(image64Data)

        # upload image to S3
        s3.put_object(
            Bucket="image-data",
            Key=f'{str(imageHash)}/dithered_image.png',
            Body=image,
            ContentType='image/png'
        )

        # upload rawData to s3
        s3.put_object(
            Bucket="image-data",
            Key=f'{str(imageHash)}/raw_data.txt',
            Body=image,
            ContentType='text/plain'
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
