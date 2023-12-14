import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'items')
table = dynamodb.Table(table_name)


def create_item(data):
    response = table.put_item(Item=data)
    return data


def read_item(item_id):
    response = table.query(KeyConditionExpression=Key('id').eq(item_id))
    item = response.get('Items', [])[0]
    return item


def update_item(item_id, data):
    response = table.update_item(
        Key={'id': item_id},
        UpdateExpression='SET #attr1 = :val1',
        ExpressionAttributeNames={'#attr1': 'attribute_name'},
        ExpressionAttributeValues={':val1': data['attribute_name']}
    )
    return data


def delete_item(item_id):
    response = table.delete_item(Key={'id': item_id})
