using System.IO.Compression;
using Amazon.S3;
using AppConfig;
using S3Library;


var s3Client = new AwsS3Client(AwsS3AppConfig.GetAppCredentials());
var s3BucketDetails = AwsS3AppConfig.GetS3BucketDetails();
try
{
    var listOfObjects = s3Client.ListItemsAsync(s3BucketDetails.bucketName, 10);
    foreach (var item in listOfObjects.Result)
    {
        var directoryToWrite = Directory.CreateDirectory($"{Directory.GetCurrentDirectory()}\\temp\\downloads\\{item.Split(".")[0]}");
        Console.WriteLine($"output directory: {directoryToWrite.FullName}");
        var response = await s3Client.GetObject("k0x-demo-download-bucket", item);
        using var zip = new ZipArchive(response.ResponseStream, ZipArchiveMode.Read);
        foreach (var entry in zip.Entries)
        {
            Console.WriteLine($" writting file {entry.Name} to output directory");
            entry.ExtractToFile($"{directoryToWrite.FullName}\\{entry.Name}");
        }
    } 
}
catch (AmazonS3Exception e)
{
    Console.WriteLine(e.Message);
}
catch(IOException e)
{
    Console.WriteLine(e.Message);
}



