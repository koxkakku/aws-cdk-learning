using System;
using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.Route53;
using Constructs;

namespace CdkTransitgateway
{
    public class CdkTransitgatewayStack : Stack
    {
        public const string SERVICE_NAME = "k0x-vpc";
        internal CdkTransitgatewayStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            int random = new Random().Next();
            int noOfSubnets = 2;
            string serviceId = $"{SERVICE_NAME}-{random}";
            string subnetName = $"{SERVICE_NAME}-private-subnet-{random}";
            string securityGroupId = $"{SERVICE_NAME}-security-group-{random}";
            string tansitGatewayId = $"{SERVICE_NAME}-transit-gateway-{random}";
            string attachmentid = $"{SERVICE_NAME}-transit-gateway-attachment-{random}";
            SubnetConfiguration[] subnetConfigurations = CreateSubnetConfig(noOfSubnets, subnetName);
            var vpc = new Vpc(this, serviceId, new VpcProps
            {
                VpcName = SERVICE_NAME,
                MaxAzs = 2,
                SubnetConfiguration = subnetConfigurations

            });

            var securityGroup = new SecurityGroup(this, securityGroupId, new SecurityGroupProps{
                Vpc = vpc
            });

            var vpcEndpoint = vpc.AddInterfaceEndpoint("s3Endpoint", new InterfaceVpcEndpointOptions{
                Service = InterfaceVpcEndpointAwsService.S3,
                Subnets = new SubnetSelection{SubnetType = SubnetType.PRIVATE_ISOLATED}
            });
    
            new VpcEndpointServiceDomainName(this, "s3EndpointDomain", new VpcEndpointServiceDomainNameProps{
                EndpointService = vpcEndpoint,
            });
            var transitGateway = new CfnTransitGateway(this, tansitGatewayId, new CfnTransitGatewayProps{
                DefaultRouteTableAssociation = "enable",
                DefaultRouteTablePropagation = "enable",
            });

            var attachment = new CfnTransitGatewayAttachment(this, attachmentid, new CfnTransitGatewayAttachmentProps{
                TransitGatewayId = transitGateway.Ref,
                VpcId = vpc.VpcId,
                SubnetIds = Array.ConvertAll(vpc.PrivateSubnets, x=>x.SubnetId.ToString())
            });

            var transitGatewayRouteTable = new CfnTransitGatewayRouteTable(this, "transitGatewayRouteTable", new CfnTransitGatewayRouteTableProps{
                TransitGatewayId = transitGateway.Ref
            });

        }
        

        private static SubnetConfiguration[] CreateSubnetConfig(int noOfSubnets, string subnetName)
        {
            SubnetConfiguration[] subnetConfigurations = new SubnetConfiguration[2];
            for (int i = 0; i < noOfSubnets; i++)
            {
                SubnetConfiguration snetConfig = new SubnetConfiguration
                {
                    CidrMask = 24,
                    Name = $"{subnetName}-{i}",
                    SubnetType = SubnetType.PRIVATE_ISOLATED,
                };
                subnetConfigurations[i] = snetConfig;
            }

            return subnetConfigurations;
        }

    }
}
