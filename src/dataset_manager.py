from AWSHandler import AWSClient
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Callable
import os
import json


class S3FileConfig(BaseModel):
    bucket_name: str = Field(..., description="The S3 bucket name")
    prefix: str = Field(..., description="The S3 prefix to list objects from")


class FileHandler:
    def __init__(self):
        self.merge_strategies: Dict[str, Callable] = {
            'merge_json_files_file_name': self._merge_json_files_file_name
            # Add more strategies here
        }

    def list_files(self, s3_config: S3FileConfig) -> List[str]:
        response = self.client.list_objects_v2(Bucket=s3_config.bucket_name, Prefix=s3_config.prefix)
        return [obj['Key'] for obj in response.get('Contents', [])][1:]
    
    def download_file(self, s3_config: S3FileConfig, s3_file_name: str, output_file_name: str):
        self.client.download_file(s3_config.bucket_name, s3_file_name, output_file_name)

    def process_files(self, s3_config: S3FileConfig, output_dir: str, fileProcessor: Callable):
        files = self.list_files(dataset)
        for s3_file_name in files:
            file_name = s3_file_name.split('/')[-1]
            output_file_name = os.path.join(output_dir, file_name)
            
            # Extract utterances and save to local file
            fileProcessor(output_file_name)
            
            print(f"Saved processed file to {output_file_name}")

    def add_merge_strategy(self, name: str, strategy: Callable):
        self.merge_strategies[name] = strategy
    

    def merge_files(self, method: str, *args, **kwargs):
        if method not in self.merge_strategies:
            raise ValueError(f"Merge method '{method}' not found.")
        return self.merge_strategies[method](*args, **kwargs)

    def _merge_json_files_file_name(self, input_folder: str, output_file: str, common_str: str):
        merged_data = []

        for filename in os.listdir(input_folder):
            if common_str in filename and filename.endswith('.json'):
                with open(os.path.join(input_folder, filename), 'r') as file:
                    data = json.load(file)
                    merged_data.extend(data)

        with open(output_file, 'w') as out_file:
            json.dump(merged_data, out_file, indent=4)

        print(f"Merged JSON data saved to {output_file}")