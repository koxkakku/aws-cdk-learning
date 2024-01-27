import json
import os

from aws_cdk import (
    # Duration,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_secretsmanager as sm,
    aws_rds as rds,
    aws_sns as sns,
    aws_ec2 as ec2,
    aws_sns_subscriptions as sns_subscriptions,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)

try:
    from aws_cdk import core as cdk
except ImportError:
    import aws_cdk as cdk

from chalice.cdk import Chalice


RUNTIME_SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, 'runtime')


class ChaliceApp(cdk.Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        # ########################
        self.vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id='vpc-08f84d09b3f9abd06')
        s3_Bucket_urn = 'arn:aws:s3:::report-bucket-17012024'
        self.s3Bucket = s3.Bucket.from_bucket_arn(self, "reportBucket", s3_Bucket_urn)
        self.snsTopic = sns.Topic.from_topic_arn(self, "snsTopic", 'arn:aws:sns:us-east-1:642252392942:report-info.fifo')
        
        self.dbSecret = sm.Secret(self, "dbSecret",
            generate_secret_string=sm.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "postgres"}),
                generate_string_key="password",
                exclude_punctuation=True,
                exclude_characters="/@\""
            )
        )
   
        self.db = rds.DatabaseInstance(self, "db",
                                  database_name="vtestreportdb",    
                                  engine=rds.DatabaseInstanceEngine.POSTGRES,
                                  credentials = rds.Credentials.from_secret(self.dbSecret),
                                  instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO), 
                                  vpc=self.vpc,
                                  vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                                  )
                
        self.sqsQueue = sqs.Queue(self, "reportQueue",
                                  queue_name="reportQueue.fifo",
                                  fifo=True,
                                  content_based_deduplication=True,
                                  retention_period=cdk.Duration.seconds(1209600),
                                  removal_policy=cdk.RemovalPolicy.DESTROY,
                                  visibility_timeout=cdk.Duration.seconds(300),
                                  )
        self.snsTopic.add_subscription(sns_subscriptions.SqsSubscription(self.sqsQueue))

        # ########################
        self.chalice = Chalice(
            self, 'ChaliceApp', source_dir=RUNTIME_SOURCE_DIR,
            stage_config={
                'environment_variables': {
                    'APP_SQS_QUEUE_ARN': self.sqsQueue.queue_arn,
                    'APP_DB_URL': self.db.db_instance_endpoint_address,
                    'APP_DB_SECRET_NAME': self.dbSecret.secret_name,
                    'DB_USER': self.dbSecret.secret_value_from_json('username').to_string(),
                    'DB_PASSWORD': self.dbSecret.secret_value_from_json('password').to_string(),
                    'S3_BUCKET_NAME': self.s3Bucket.bucket_name,
                }
            }
        )
        self.sqsQueue.grant_consume_messages(self.chalice.get_role('DefaultRole'))
        self.s3Bucket.grant_read_write(self.chalice.get_role('DefaultRole'))