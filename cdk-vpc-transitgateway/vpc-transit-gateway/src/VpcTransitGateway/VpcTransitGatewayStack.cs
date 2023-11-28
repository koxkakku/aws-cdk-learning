using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.TransitGateway;
using Amazon.CDK.AWS.TransitGatewayConnect;
using Amazon.CDK.Json;
using Constructs;

namespace VpcTransitGateway
{
    public class VpcTransitGatewayStack : Stack
    {
        internal VpcTransitGatewayStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            // The code that defines your stack goes here
            var accountA = Node.TryGetContext("account_a").ToString();
            var accountB = Node.TryGetContext("account_b").ToString();
            var vpcEndpointACidr = Node.TryGetContext("vpc_endpoint_a_cidr").ToString();
            var vpcEndpointBCidr = Node.TryGetContext("vpc_endpoint_b_cidr").ToString();
            var vpcEndpointSgIngressPorts = Node.TryGetContext("vpc_endpoint_sg_ingress_ports").ToString().Split(",");
            var vpcEndpointSgEgressPorts = Node.TryGetContext("vpc_endpoint_sg_egress_ports").ToString().Split(",");

            // Create the Transit Gateway
            var transitGateway = new TransitGateway(this, "MyTransitGateway", new TransitGatewayProps
            {
                defaultRouteTableAssociation = DefaultRouteTableAssociation.ENABLED,
                defaultRouteTablePropagation = DefaultRouteTablePropagation.ENABLED,
            });
        }
    }
}
