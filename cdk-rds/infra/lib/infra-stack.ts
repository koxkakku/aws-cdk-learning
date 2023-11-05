import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';




export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });

    // create S3 bucket
    const bucket = new s3.Bucket(this, 'InfraBucket', {
      bucketName: 'my-bucket-name',
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })

    // create vpc 
    const vpc = new ec2.Vpc(this, 'InfraVpc', {
      ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
      natGateways: 0,
      vpcName: 'my-vpc-name',
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'ingress' ,
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 28,
          name: 'rds',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,

        },
        {
          cidrMask: 24,
          name: 'application',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,

        }
      ]
    })

    //create rds 
    const rdsInstance = new rds.DatabaseInstance(this,'Rds',{
      instanceIdentifier: 'my-rds-instance',
      engine: rds.DatabaseInstanceEngine.MYSQL,
      vpc:vpc,
      databaseName: 'my-database-name',
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED},
    })
      
  }
}
