using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VpceApp.model
{
    public class ConfigProps
    {
        [JsonProperty("vpceAppConfig")] public VpcAppConfig vpcAppConfig {  get; set; } 

    }
}
