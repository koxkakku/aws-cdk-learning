import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { readFileSync } from 'fs';

export class WebserverStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'WebserverQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
    // ec2 vpc
    const vpc_ec2 = new ec2.Vpc(this, 'WebserverVpc', { 
      vpcName: 'web-server-vpc',
      ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
      natGateways:0,
    })
    // vpc security group
    const vpc_SG = new ec2.SecurityGroup(this, 'WebserverSecurityGroup', {
      securityGroupName: 'web-server-security-group',
      vpc: vpc_ec2,
      allowAllOutbound: true,

    })

    vpc_SG.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP Access')

    // ec2 instance
    const ec2Instance = new ec2.Instance(this, 'WebserverInstance', {
      instanceName: 'web-server-instance',
      vpc: vpc_ec2,
      securityGroup: vpc_SG,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
      machineImage: ec2.MachineImage.latestAmazonLinux2(),
      keyName: 'kox-ec2-kp',
      
    })
    ec2Instance.addUserData(readFileSync('./lib/user-data.sh', 'utf8'))
    
    
      

  }
}
