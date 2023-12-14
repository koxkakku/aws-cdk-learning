from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_apigateway import LambdaRestApi
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType
from aws_cdk import Stack
from constructs import Construct

class PoetryChaliceDynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # Create a DynamoDB table
        my_table = Table(
            self, 'poetry_chalice_dynamodb',
            partition_key=Attribute(name='id', type=AttributeType.STRING),
            read_capacity=5,
            write_capacity=5
        )

        # Create a Lambda function from the Chalice app
        chalice_function = Function(
            self, 'MyChaliceFunction',
            runtime=Runtime.PYTHON_3_11,
            handler='app',
            code=Code.from_asset('crud-dynamodb'),
            environment={
                'DYNAMODB_TABLE': my_table.table_name
            }
        )

        # Grant the Lambda function permission to access the DynamoDB table
        my_table.grant_read_write_data(chalice_function)

        # Create an API Gateway and associate it with the Lambda function
        api = LambdaRestApi(
            self, 'poetry-chalice-api',
            handler=chalice_function
        )