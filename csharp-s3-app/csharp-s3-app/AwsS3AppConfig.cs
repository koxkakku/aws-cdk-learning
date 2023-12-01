using Amazon.Runtime;
using csharp_s3_app;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AppConfig
{
    public class AwsS3AppConfig
    {
        public static AWSCredentials GetAppCredentials()
        {
            AwsConfig awsConfig = LoadAwsConfig();
            AWSCredentials basicAWSCredentials = new BasicAWSCredentials(
                awsConfig.awsAccessKeyId, awsConfig.awsSecretAccessKey
                );
            return basicAWSCredentials;
        }

        private static AwsConfig LoadAwsConfig()
        {
            IConfigurationRoot configurationConfig = new ConfigurationBuilder()
                                            .SetBasePath(Directory.GetParent(AppContext.BaseDirectory).FullName)
                                            .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
                                            .Build();
            AwsConfig awsConfig = new();
            configurationConfig.GetSection("AwsConfig").Bind(awsConfig);
            return awsConfig;
        }
        public static S3Bucket GetS3BucketDetails()
        {
            IConfigurationRoot configurationConfig = new ConfigurationBuilder()
                                            .SetBasePath(Directory.GetParent(AppContext.BaseDirectory).FullName)
                                            .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
                                            .Build();
            S3Bucket S3bucketConfig = new();
            configurationConfig.GetSection("S3Bucket").Bind(S3bucketConfig);
            return S3bucketConfig;
        }

    }
}
