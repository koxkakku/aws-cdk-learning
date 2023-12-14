import os
import boto3
from chalice import Chalice


app = Chalice(app_name='poetry-chalice-cdk-app')
dynamodb = boto3.resource('dynamodb')
dynamodb_table = dynamodb.Table(os.environ.get('APP_TABLE_NAME', ''))


@app.route('/users', methods=['POST'])
def create_user():
    request = app.current_request.json_body
    item = {
        'PK': 'User#%s' % request['username'],
        'SK': 'Profile#%s' % request['username'],
    }
    item.update(request)
    dynamodb_table.put_item(Item=item)
    return {}


@app.route('/users/{username}', methods=['GET'])
def get_user(username):
    key = {
        'PK': 'User#%s' % username,
        'SK': 'Profile#%s' % username,
    }
    item = dynamodb_table.get_item(Key=key)['Item']
    del item['PK']
    del item['SK']
    return item

@app.route('/users/{username}', methods=['PUT'])
def update_item(username):
    request = app.current_request.json_body
    key = {
        'PK': 'User#%s' % username,
        'SK': 'Profile#%s' % username,
    }
    
    item = dynamodb_table.update_item(Key=key,
                                       UpdateExpression='SET #name = :name, #email = :email',
                                       ExpressionAttributeNames={'#name': 'name', '#email': 'email'},
                                       ExpressionAttributeValues={':name': request['name'], ':email': request['email']})
    return {'item': item}