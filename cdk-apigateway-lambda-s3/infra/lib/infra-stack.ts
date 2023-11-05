import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cdk_iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

 
export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });

    //s3 bucket
    const bucket = new s3.Bucket(this, 'InfraBankingBucket', {
      bucketName:'infra-banking-bucket',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects:true
    });

    const iamrole = new cdk_iam.Role(this, 'InfraBankingLambdaRole', {
      roleName: 'infra-banking-lambda-role',
      description: 'IAM role for banking app',
      assumedBy: new cdk_iam.ServicePrincipal('lambda.amazonaws.com')

    });
    iamrole.addManagedPolicy(cdk.aws_iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'))

    const infraBankinglambda = new lambda.Function(this, 'InfraBankingLambda', {
      functionName: 'infra-banking-lambda',
      runtime: lambda.Runtime.PYTHON_3_11,
      code: lambda.Code.fromAsset('../services/'),
      handler: 'lambda_function.lambda_handler',
      timeout: cdk.Duration.seconds(300),
      role: iamrole
    })

    const infraBankingApiGateway = new apigateway.LambdaRestApi(this, 'InfraBankingApiGateway', {
      restApiName: 'infra-banking-apiGateway',
      handler: infraBankinglambda,
      proxy: false,
      deploy: true,
      deployOptions: {
        stageName: 'dev'
      }
    })

    const infraBankingResource = infraBankingApiGateway.root.addResource('bank-account-status')
    infraBankingResource.addMethod('GET')
  }

} 
