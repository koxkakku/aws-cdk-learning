# from sqlalchemy import event
# import os
# import logging
# import sqlalchemy
# import boto3
# import base64
# import json
# from botocore.exceptions import ClientError

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# class DB:
#     __instance = None

#     def __init__(self, secret_name):
#         """ Virtually private constructor. """
#         self.secret_name = secret_name
#         if DB.__instance is not None:
#             raise Exception(
#                 "This class is a singleton, use DB.create()")
#         else:
#             DB.__instance = self
#         self.engine = self.create_engine()

#     @staticmethod
#     def create(secret_name):
#         if DB.__instance is None:
#             DB.__instance = DB(secret_name)

#         return DB.__instance

#     @staticmethod
#     def getInstance():
#         return DB.__instance
#     @staticmethod
#     def get_secret(secret_name):
#         client = boto3.client('secretsmanager')

#         try:
#             get_secret_value_response = client.get_secret_value(
#                 SecretId=secret_name
#             )
#         except ClientError as e:
#             if e.response['Error']['Code'] == 'DecryptionFailureException':
#                 raise e
#             elif e.response['Error']['Code'] == 'InternalServiceErrorException':
#                 raise e
#             elif e.response['Error']['Code'] == 'InvalidParameterException':
#                 raise e
#             elif e.response['Error']['Code'] == 'InvalidRequestException':
#                 raise e
#             elif e.response['Error']['Code'] == 'ResourceNotFoundException':
#                 raise e
#         else:
#             if 'SecretString' in get_secret_value_response:
#                 secret = get_secret_value_response['SecretString']
#             else:
#                 secret = base64.b64decode(get_secret_value_response['SecretBinary'])

#             return json.loads(secret)

#     def get_credentials(secret_name):
#         """ Fetch credentials from either environment variables (for testing) or AWS Secret Manager"""
#         if secret_name is None:
#             return {
#                 'username': os.getenv('POSTGRESQL_USER', 'postgres'),
#                 'password': os.getenv('POSTGRESQL_PASSWORD', 'some_password'),
#                 'host': os.getenv('POSTGRESQL_HOST', 'localhost'),
#                 'port': os.getenv('POSTGRESQL_PORT', 5432),
#                 'database': os.getenv('POSTGRESQL_DATABASE', 'user_database'),
#                 'engine': 'postgresql',
#             }

#         # get all access credentials from secrets manager
#         credentials = DB.get_secret(secret_name)
#         if credentials is not None:
#             return {
#                 'username': credentials['username'],
#                 'password': credentials['password'],
#                 'host': credentials['host'],
#                 'port': credentials['port'],
#                 'database': credentials['dbname'],
#                 # 'engine': credentials['engine'],
#                 'engine': 'postgresql',
                
#             }

#     def create_engine(self):
#         credentials = DB.get_credentials(self.secret_name)
#         print("cred %s", credentials)
#         if credentials is not None:
#             return sqlalchemy.create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
#                 engine=credentials['engine'],
#                 user=credentials['username'],
#                 password=credentials['password'],
#                 host=credentials['host'],
#                 port=int(credentials['port']),
#                 database=credentials['database']
#             ),
#                 pool_size=200,
#                 max_overflow=0,
#                 echo=bool(os.getenv('POSTGRESQL_DEBUG', False))
#             )

#     def connect(self):
#         return self.engine.connect()