import json
import boto3

client = boto3.client('s3')

def lambda_handler(event, context):
    response= client.get_object(Bucket='infra-banking-bucket', Key='banking-info.json')
    dataByte = response['Body'].read()
    dataString = dataByte.decode('utf-8')
    dataDict = json.loads(dataString)
    return {
        'statusCode': 200,
        'body': dataDict,
        'body': json.dumps(dataDict),
        'headers': {'Content-Type': 'application/json'}
    }
