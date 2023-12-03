using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
using Amazon.CDK.AWS.Route53;
using CloudVpceApp.model;
using Constructs;
using Amazon.CDK.AWS.Route53.Targets;
using Newtonsoft.Json;
using System;

namespace CloudVpceApp
{
    public class CloudVpceAppStack : Stack
    {
        internal CloudVpceAppStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
           // The code that defines your stack goes here
            var contextLocal = this.Node.TryGetContext("VpceAppConfig");
            var context = JsonConvert.DeserializeObject<VpceAppConfig>(JsonConvert.SerializeObject(contextLocal));
            var appName = context.AppName;
            var vpc = Vpc.FromLookup(this,$"{appName}-vpc",new VpcLookupOptions
            {
                VpcId = context.vpcId
            });
            var securityGroup = new SecurityGroup(this, $"{appName}-sg", new SecurityGroupProps
            {
                AllowAllOutbound = true,
                Vpc = vpc
            });
            foreach (int portNo in context.vpceConfig.OpenPorts)
            {
                securityGroup.AddIngressRule(Peer.Ipv4(vpc.VpcCidrBlock), Port.Tcp(portNo));
            }

            var vpcendpoint = new InterfaceVpcEndpoint(this, $"{appName}-vpce",
                new InterfaceVpcEndpointProps
                {
                    Subnets = new SubnetSelection { SubnetType = SubnetType.PRIVATE_ISOLATED },
                    Vpc = vpc,
                    Service = new InterfaceVpcEndpointAwsService(context.vpceConfig.ServiceName),
                    PrivateDnsEnabled = false,
                    SecurityGroups = [securityGroup]
                });
            
            foreach(var routeConfig in context.route53Configs)
            {
                var hosted_zone = new HostedZone(this,$"zone-{appName}-{routeConfig.HostedZone}",
                    new HostedZoneProps
                    {
                        ZoneName = routeConfig.HostedZone,
                        Vpcs = [vpc]
                    });
                CreateDnsARecord(vpcendpoint, routeConfig, hosted_zone,appName);
            }
        }

        private void CreateDnsARecord(InterfaceVpcEndpoint vpcendpoint, Route53Config routeConfig, HostedZone hosted_zone, string appName)
        {
            foreach (var arecord in routeConfig.DnsARecords)
            {
                var aRecord = new ARecord(this, $"aRecord-{appName}-{arecord}",
                    new ARecordProps
                    {
                        Zone = hosted_zone,
                        RecordName = arecord,
                        Target = RecordTarget.FromAlias(new InterfaceVpcEndpointTarget(vpcendpoint))
                    });
            }
        }

    }
}
