from aws_cdk import aws_ec2 as ec2

VPC = 'k0x-vpc'
REGION = 'us-east-1'
VPC_CIDR = '10.0.0.0/16'
EIP = 'k0x-eip'
VPC_GATEWAY_ATTACHMENT = 'k0x-vpc-gateway-attachment'

INET_GATEWAY = 'k0x-internet-gateway'
NAT_GATEWAY = 'k0x-nat-gateway'

PUBLIC_SUBNET = 'k0x-public-subnet'
PRIVATE_SUBNET = 'k0x-private-subnet'

PRIVATE_ROUTE_TABLE = 'k0x-private-route-table'
PUBLIC_ROUTE_TABLE = 'k0x-public-route-table'

ROUTE_TABLES_ID_TO_ROUTE_MAP = {
    PUBLIC_ROUTE_TABLE:[ 
    {
        'destination_cidr_block': '0.0.0.0/0',
        'gateway_id': INET_GATEWAY,
        'router_type': ec2.RouterType.GATEWAY
    }],
    PRIVATE_ROUTE_TABLE: [{
        'destination_cidr_block': '0.0.0.0/0',
        'gateway_id': NAT_GATEWAY,
        'router_type': ec2.RouterType.NAT_GATEWAY
    }]
}

SUBNET_CONFIGURATION = {
    PUBLIC_SUBNET: {
        'cidr_block': '10.0.1.0/24',
        'availabilityZone': f'{REGION}a',
        'mapPublicIpOnLaunch': True,
        'route_table_id' : PUBLIC_ROUTE_TABLE
    },
    PRIVATE_SUBNET: {
        'cidr_block': '10.0.2.0/24',
        'availabilityZone': f'{REGION}b',
        'mapPublicIpOnLaunch': False,
        'route_table_id': PRIVATE_ROUTE_TABLE
    }
}

