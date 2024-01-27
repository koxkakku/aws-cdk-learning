import json
import os
import boto3
import sqlalchemy
import base64
from chalice import Chalice
from chalice.app import SQSEvent
from sqlalchemy.orm import sessionmaker
from chalicelib.session import SessionHandler
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from botocore.exceptions import ClientError

app = Chalice(app_name='chaliceCdkReportApp')
s3 = boto3.client('s3')
postgres_db_secret_name = os.environ.get('APP_DB_SECRET_NAME', '')
s3_Bucket_name = os.environ.get('S3_BUCKET_NAME', '')
sqsQueueArn = os.environ.get('APP_SQS_QUEUE_ARN', '')
client = boto3.client('secretsmanager')
# ##########################################################
def create_engine(credentials):
        print(credentials)
        print("cred %s", credentials)
        if credentials is not None:
            return sqlalchemy.create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
                # engine=credentials['engine'],
                engine='postgresql',
                user=credentials['username'],
                password=credentials['password'],
                host=credentials['host'],
                port=int(credentials['port']),
                database=credentials['dbname']
            ),
                pool_size=200,
                max_overflow=0,
                echo=bool(os.getenv('POSTGRESQL_DEBUG', False))
            )
    
def get_secret(secret_name):
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

            return json.loads(secret)    
# #################################################################

cred = get_secret(secret_name = postgres_db_secret_name)
db = create_engine(credentials=cred)

@app.on_sqs_message(queue_arn= sqsQueueArn)
def handle_message(event: SQSEvent):
 
    print(f"event is{event}")
    for record in event: 
        jsonBody = json.loads(record.body)
        app.log.info("Received message with contents: %s", jsonBody)
        print("Received message with contents: %s", jsonBody)
        message =  json.loads(jsonBody['Message'])
        app.log.info("Received message : %s", message)
        print("Received message : %s", message)
        jobid=message["job_id"]
        testRunId = message["test_run_id"]
        testDefId= message["test_definition_id"]
        app.log.info(f"job_id:{jobid},test_run_id: {testRunId}, test_definition_id: {testDefId}")
        print(f"job_id:{jobid},test_run_id: {testRunId}, test_definition_id: {testDefId}" )
        
        response = s3.list_objects_v2(
            Bucket=s3_Bucket_name,
            Prefix =f"{jobid}/{testRunId}/{testDefId}"
            )
        app.log.info(f"response list obj v2:{response}")
        print(f"response list obj v2:{response}")
        if "Contents" not in response:
            app.log.info("No objects found")
            print("No objects found")
            return
        for obj in response["Contents"]:            
            key = obj["Key"]
            app.log.info("key: %s",key)
            print(key)
            if key.endswith('.json'):
                jsonFile=s3.get_object(Bucket = s3_Bucket_name,Key= key)
                print(jsonFile)
                data = json.loads(jsonFile["Body"].read())
                print(data)
                createReport(data)
# ######################################################
def createReport(report):
    engine = db.engine
    print('engine %s', engine)
    Session = sessionmaker(bind=engine)
    print(session)
    session = Session()

    try:
        print(report)
        report_session = SessionHandler.create(session, Report)
        print(1)
        # add a new record
        report_session.add(report)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# ##########################################################
Base = declarative_base()
@dataclass
class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String)
    customer_name = Column(String)
    account_number = Column(String)
    account_balance = Column(String)

# create table if it does not exist, if you change the model,
#  you have to drop the table first for this code to alter it in the db
if db is not None:
    engine = db.engine
    if engine is not None:
        Base.metadata.create_all(engine)

