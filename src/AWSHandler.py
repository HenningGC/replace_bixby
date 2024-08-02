from pydantic import BaseModel, Field, SecretStr
from typing import Literal, Optional, Dict
import os
import boto3
from botocore.client import BaseClient


class AWSClientConfig(BaseModel):
    service_name: Literal['s3', 'sagemaker'] = Field(..., description="The AWS service name")
    region_name: str = Field(..., description="The AWS region name")
    aws_access_key_id: Optional[SecretStr] = Field(None, description="The AWS access key ID")
    aws_secret_access_key: Optional[SecretStr] = Field(None, description="The AWS secret access key")

class AWSClient:
    
    def __init__(self, config: AWSClientConfig):
        self.config = config
        self.client = self._create_client()


    def _create_client(self) -> BaseClient:
        client_params = {
            "service_name": self.config.service_name,
            "region_name": self.config.region_name
        }

        if self.config.aws_access_key_id and self.config.aws_secret_access_key:
            client_params.update({
                "aws_access_key_id": self.config.aws_access_key_id.get_secret_value(),
                "aws_secret_access_key": self.config.aws_secret_access_key.get_secret_value()
            })

        return boto3.client(**client_params)

    def get_client(self) -> BaseClient:
        return self.client


class S3Downloader:

    def __init__(self, bucket_name: str, prefix: str, output_dir: str, config: AWSClientConfig):
        load_dotenv(find_dotenv())
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.output_dir = output_dir
        self.s3_client = AWSClient(config=config).get_client()


    def list_files(self):
        response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        return [obj['Key'] for obj in response.get('Contents', [])][1:]

    def download_file(self, s3_file_name: str, output_file_name: str):
        self.s3_client.download_file(bucket_name, s3_file_name, output_file_name)

    def process_files(self,fileProcessor):
        files = self.list_files()

        for s3_file_name in files:
            file_name = s3_file_name.split('/')[-1]
            output_file_name = self.output_dir
            self.download_file(s3_file_name, output_file_name)
            fileProcessor(output_file_name)
