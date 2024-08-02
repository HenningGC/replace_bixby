from AWSClientService import AWSClientConfig, AWSClient
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
import os


def main():
    load_dotenv()
    config = AWSClientConfig(
        service_name='s3',
        region_name = os.getenv('AWS_REGION'),
        aws_access_key_id = SecretStr(os.getenv('AWS_ACCESS_KEY')),
        aws_secret_access_key = SecretStr(os.getenv('AWS_SECRET_KEY'))
    )
    S3Client = AWSClient(config=config).get_client()
    print(S3Client.list_buckets())
    

if __name__ == "__main__":
    main()
