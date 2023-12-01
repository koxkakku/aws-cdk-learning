using System;
using System.IO.Compression;
using System.Net;
using System.Threading.Tasks;
using Amazon.Runtime;
using Amazon.S3;
using Amazon.S3.Model;

namespace S3Library
{
    public class AwsS3Client(AWSCredentials credentials)
    {
        private readonly AWSCredentials _credentials = credentials;

        public async Task<GetObjectResponse> GetObject(string bucketName, string objectKey)
        {
            var amazonS3Client = new AmazonS3Client(_credentials);
            var request = new GetObjectRequest
            {
                BucketName = bucketName,
                Key = objectKey
            };

            return await amazonS3Client.GetObjectAsync(request);
        }

        public async Task<List<string>> ListItemsAsync(string bucketName, int? maxItems = null)
        {
            List<string> listOfObjects = new List<string>();
            using (var amazonS3Client = new AmazonS3Client(_credentials))
            {
                var request = new Amazon.S3.Model.ListObjectsV2Request
                {
                    BucketName = bucketName,
                    MaxKeys = 10,
                };
                ListObjectsV2Response response;

                do
                {
                    response = await amazonS3Client.ListObjectsV2Async(request);
                    foreach (S3Object entry in response.S3Objects)
                    {
                        if(entry.Key != null && entry.Key.EndsWith(".zip"))
                        {
                            Console.WriteLine($"key = {entry.Key} :  size = {entry.Size}");
                            listOfObjects.Add(entry.Key);
                        }
                        
                    }
                    request.ContinuationToken = response.NextContinuationToken;
                    
                } while (response.IsTruncated);
            }

            return (listOfObjects);
        }
    }
}