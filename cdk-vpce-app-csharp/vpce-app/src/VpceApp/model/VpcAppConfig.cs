using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VpceApp.model
{
    public class VpcAppConfig
    {
        public VpcAppConfig()
        {
        }
        [JsonProperty("env")] public AwsEnv Env { get; set; }
        [JsonProperty("vpceConfig")] public VpceConfig vpceConfig { get; set; }
        [JsonProperty("vpcId")] public string vpcId { get; set; }

    }
   
}
