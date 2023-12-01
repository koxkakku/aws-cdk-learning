using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.Route53;
using Constructs;
using VpceApp.model;

namespace VpceApp
{
    public class VpceAppStack : Stack
    {
        public VpceAppStack(Constructs.Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            // The code that defines your stack goes here
            var context = (VpcAppConfig)this.Node.TryGetContext("VpceAppConfig");
            var vpc = Vpc.FromLookup(this,"Existing-VPC",new VpcLookupOptions
            {
                VpcId = context.vpcId
            });
            var securityGroup = new SecurityGroup(this, "k0x-demo-vpce-sg", new SecurityGroupProps
            {
                AllowAllOutbound = true,
                Vpc = vpc
            });
            foreach (int portNo in context.vpceConfig.OpenPorts)
            {
                securityGroup.AddIngressRule(Peer.Ipv4(vpc.VpcCidrBlock), Port.Tcp(portNo));
            }

            var vpcendpoint = new InterfaceVpcEndpoint(this, "k0x-demo-vpce",
                new InterfaceVpcEndpointProps
                {
                    Subnets = new SubnetSelection { SubnetType = SubnetType.PRIVATE_ISOLATED },
                    Vpc = vpc,
                    PrivateDnsEnabled = false,
                    SecurityGroups = [securityGroup]
                });
            
            foreach(string hostezone in context.vpceConfig.HostedZones)
            {
                new HostedZone(this, "AbcHostedZone",

                   new HostedZoneProps
                   {
                       ZoneName = hostezone,
                       Vpcs = [vpc]
                   }
                   );
            }
            
           
                
        }
    }
}
