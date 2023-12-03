using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CloudVpceApp.model
{
    public class VpceAppConfig
    {
        public VpceAppConfig()
        {
        }
        [JsonProperty("appName")] public string AppName { get; set; }
        [JsonProperty("vpceConfig")] public VpceConfig vpceConfig { get; set; }
        [JsonProperty("vpcId")] public string vpcId { get; set; }
        [JsonProperty("route53Config")] public List<Route53Config> route53Configs { get; set; }

    }
   
}
