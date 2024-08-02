from pydantic import BaseModel, Field, SecretStr
from typing import Literal, Optional
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