using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VpceApp.model
{
    public class AwsEnv
    {
        public AwsEnv()
        {
        }

        [JsonProperty("account")] public string account {  get; set; }
        [JsonProperty("region")] public string region { get; set; }
    }
}
