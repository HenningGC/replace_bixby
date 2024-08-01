from utils.AWSClientService import AWSService


def main():
    
    S3Client = AWSService('s3').client
    print(S3Client.list_buckets())
    

if __name__ == "__main__":
    main()
