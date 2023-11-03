import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
    
    // dynamo db 
    const dynmodb = new dynamodb.Table(this,'infra-dynamo-db', {
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.NUMBER
      },
      readCapacity:3,
      writeCapacity:3,
      tableName:'infra-dynamo-db-table',
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
  }
}
