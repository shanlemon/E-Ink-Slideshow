import os

import boto3
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


USERS_TABLE = os.environ['USERS_TABLE']

# Upload Image to S3
# @app.route('/upload', methods=['POST'])
# def upload_image(image_data):
    

@app.route('', methods=['GET'])
def default():
    return jsonify({'message': 'Hello World!'})

# # Edit 
# @app.route('edit', methods=['POST'])
# def edit_slideshow(user_id, next_idx, ids):
#     try:
#         response = dynamodb_client.update_item(
#             TableName=USERS_TABLE,
#             Key={
#                 'user_id': {'S': user_id}
#             },
#             UpdateExpression="SET next_idx = :next_idx, raw_data = :raw_data, images = :images",
#             ExpressionAttributeValues={
#                 ':next_idx': {'N': next_idx},
#                 ':raw_data': {'S': raw_data},
#                 ':images': {'S': images}
#             },
#             ReturnValues="UPDATED_NEW"
#         )
#         return make_response(jsonify({'status': 'success'}), 200)
#     except Exception as e:
#         return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)


# # Get hex value of next image
# @app.route('next-image', methods=['GET'])
# def get_next_image(user_id):
#     response = dynamodb_client.get_item(
#         TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
#     )
    
#     if 'Item' not in response or 'next_idx' not in response['Item'] or 'raw_data' not in response['Item']:
#         return make_response(jsonify({'error': 'Image not found'}), 404)

#     # get next index from response
#     next_index = response['Item']['next_idx']['N']

#     # increment next index in table
#     dynamodb_client.update_item(
#         TableName=USERS_TABLE,
#         Key={'userId': {'S': user_id}},
#         UpdateExpression="set next_idx = next_idx + :i",
#         ExpressionAttributeValues={':i': {'N': '1'}},
#     )

#     # get raw data at next index
#     raw_data = response['Item']['raw_data']['L'][next_index]['L']

#     # return raw data
#     return jsonify(raw_data)


# @app.errorhandler(404)
# def resource_not_found(e):
#     return make_response(jsonify(error='Not found!'), 404)



# @app.route('/users/<string:user_id>')
# def get_user(user_id):
#     result = dynamodb_client.get_item(
#         TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
#     )
#     item = result.get('Item')
#     if not item:
#         return jsonify({'error': 'Could not find user with provided "userId"'}), 404

#     return jsonify(
#         {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
#     )


# @app.route('/users', methods=['POST'])
# def create_user():
#     user_id = request.json.get('userId')
#     name = request.json.get('name')
#     if not user_id or not name:
#         return jsonify({'error': 'Please provide both "userId" and "name"'}), 400

#     dynamodb_client.put_item(
#         TableName=USERS_TABLE, Item={'userId': {'S': user_id}, 'name': {'S': name}}
#     )

#     return jsonify({'userId': user_id, 'name': name})