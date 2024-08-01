import boto3
import os
from dotenv import load_dotenv

class AWSClient:

    def __init__(self, service):

        self.service = service

    def create_client(self):

        load_dotenv()
        self._aws_client = boto3.client(
            self.service, 
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
    @property
    def aws_client(self):
        return self._aws_client

