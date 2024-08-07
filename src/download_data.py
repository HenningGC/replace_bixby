from AWSHandler import AWSClient
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List
import os


class S3FileConfig(BaseModel):
    bucket_name: str = Field(..., description="The S3 bucket name")
    prefix: str = Field(..., description="The S3 prefix to list objects from")
    output_dir: str = Field(..., description="The local directory to save the downloaded files")
    contain_str: str = Field("", description="String that the file name should contain")
    extension: str = Field("", description="File extension to filter by")

class DataDownloader:

    @staticmethod
    def list_files_in_s3(aws_client: AWSClient, s3_config: S3FileConfig) -> List[str]:
        response = aws_client.list_objects_v2(Bucket=s3_config.bucket_name, Prefix=s3_config.prefix)
        return [obj['Key'] for obj in response.get('Contents', []) if s3_config.contain_str in obj['Key'].split('/')[-1] and obj['Key'].endswith(s3_config.extension)]

    @staticmethod
    def download_from_s3(aws_client: AWSClient, s3_config: S3FileConfig, s3_file_name: str, output_file_name: str):
        aws_client.download_file(s3_config.bucket_name, s3_file_name, output_file_name)

    @classmethod
    def download_data(cls, aws_client: AWSClient, s3_config: S3FileConfig):
        files = cls.list_files_in_s3(aws_client, s3_config)
        for s3_file_name in files:
            file_name = s3_file_name.split('/')[-1]
            output_file_name = os.path.join(s3_config.output_dir, f"downloaded_{file_name}")

            # Download the file from S3
            cls.download_from_s3(aws_client, s3_config, s3_file_name, output_file_name)

            print(f"Downloaded file {file_name} to {s3_config.output_dir}")