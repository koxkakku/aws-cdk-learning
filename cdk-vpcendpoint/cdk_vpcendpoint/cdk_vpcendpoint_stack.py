import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from constructs import Construct



# Replace 'YOUR_VPC_ID' with the ID of your existing VPC
existing_vpc_id = 'vpc-00e2da4df3a6ea96c'

class CdkVpcendpointStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Import existing VPC
        existing_vpc = ec2.Vpc.from_lookup(self, 'ExistingVpc', vpc_id=existing_vpc_id)

        # Define the subnet selection criteria
       
        # Filter private subnets from existing VPC
        # Select private subnets based on the specified criteria
        subnet_selection = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        # Wrap the subnet selection criteria in a sequence
        subnets = [subnet_selection]
        # Create VPC endpoint
        vpc_endpoint = ec2.GatewayVpcEndpoint(self, 'k0x-demo-vpce', service=ec2.GatewayVpcEndpointAwsService.S3, subnets=subnets, vpc=existing_vpc, )

        # Create security group for VPC endpoint
        security_group = ec2.SecurityGroup(self, 'k0x-demo-vpce-sg', vpc=existing_vpc, allow_all_outbound=True)
        security_group.add_ingress_rule(ec2.Peer.ipv4(existing_vpc.vpc_cidr_block), ec2.Port.tcp(443))
        security_group.add_ingress_rule(ec2.Peer.ipv4(existing_vpc.vpc_cidr_block), ec2.Port.tcp(7999))

        # Create hosted zones
        abc_hosted_zone = route53.HostedZone(self, 'AbcHostedZone', zone_name='abc.com')
        xyz_hosted_zone = route53.HostedZone(self, 'XyzHostedZone', zone_name='xyz.com')

        # Create A records
        qwe_abc_record = route53.ARecord(self, 'QweAbcRecord', zone=abc_hosted_zone, record_name='qwe.abc.com', target=route53.RecordTarget.from_alias(route53_targets.InterfaceVpcEndpointTarget(vpc_endpoint)))
        rty_xyz_record = route53.ARecord(self, 'RtyXyzRecord', zone=xyz_hosted_zone, record_name='rty.xyz.com', target=route53.RecordTarget.from_alias(route53_targets.InterfaceVpcEndpointTarget(vpc_endpoint)))