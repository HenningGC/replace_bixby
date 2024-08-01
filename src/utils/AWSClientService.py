import boto3
import os
from dotenv import load_dotenv, find_dotenv

class AWSService:
    """
    A class to create AWS service clients using boto3.
    """

    def __init__(self, service):
        self.service = service
        self.client = None
        print('shit')
        dotenv_path = find_dotenv()
        if dotenv_path:
            load_dotenv(dotenv_path)
        else:
            print("Warning: .env file not found. Ensure environment variables are set.")

        aws_access_key = os.getenv('AWS_ACCESS_KEY')
        aws_secret_key = os.getenv('AWS_SECRET_KEY')
        aws_region = os.getenv('AWS_REGION')

        if not aws_access_key or not aws_secret_key or not aws_region:
            raise ValueError("AWS credentials or region are not set in environment variables.")

        self.client = boto3.client(
            self.service,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )