import aws_cdk as core
import aws_cdk.assertions as assertions

from poetry_chalice_dynamodb.poetry_chalice_dynamodb_stack import PoetryChaliceDynamodbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in poetry_chalice_dynamodb/poetry_chalice_dynamodb_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PoetryChaliceDynamodbStack(app, "poetry-chalice-dynamodb")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
