using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CloudVpceApp.model
{
    public class Route53Config
    {
        public Route53Config()
        {
        }
        [JsonProperty("hostedZone")] public string HostedZone { get; set; }
        [JsonProperty("dnsARecords")] public List<string> DnsARecords { get; set; }

    }
   
}