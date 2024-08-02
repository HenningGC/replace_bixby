from AWSHandler import AWSClientConfig, AWSClient
from file_handler import FileHandler, S3FileConfig
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
import os



def list_files_in_s3(client, bucket_name, prefix):
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return [obj['Key'] for obj in response.get('Contents', [])][1:]

def download_from_s3(client, bucket_name, s3_file_name, output_file_name):
    client.download_file(bucket_name, s3_file_name, output_file_name)


def download_data():
    load_dotenv()

    s3_client = AWSClient(config=AWSClientConfig(
        service_name='s3',
        region_name = os.getenv('AWS_REGION'),
        aws_access_key_id = SecretStr(os.getenv('AWS_ACCESS_KEY')),
        aws_secret_access_key = SecretStr(os.getenv('AWS_SECRET_KEY')))).get_client()

    bucket_name = 'asrapp-audios'
    files = list_files_in_s3(s3_client, bucket_name, 'instruction_audio/')

    for s3_file_name in files:
        file_name = s3_file_name.split('/')[-1]
        output_file_name = f"data/utterances_{file_name}"
        
        # Download the file from S3
        download_from_s3(s3_client, bucket_name, s3_file_name, output_file_name)

        print(f"Extracted and saved utterances to {output_file_name}")



    
# Takes a configuration profile with bucket name, outputdir etc.
if __name__ == "__main__":
    download_data()
