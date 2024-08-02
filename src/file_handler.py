from AWSHandler import AWSClient
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Callable
import os
import json


class FileHandler:
    def __init__(self, client, config):
        self.merge_strategies: Dict[str, Callable] = {
            'merge_json_files_file_name': self._merge_json_files_file_name,
            'merge_two_json_files': self._merge_two_json_files,
        }

    def process_files(self, input_dir: str, output_dir: str, fileProcessor: Callable):

        for file_name in os.listdir(input_dir):
            file_name = file_name.split('/')[-1]
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

    def _merge_two_json_files(self, input_file_1: str, input_file_2: str, output_file: str):
        merged_data = []
        with open(input_file_1, 'r') as file1:
            data1 = json.load(file1)
            merged_data.extend(data1)

        with open(input_file_2, 'r') as file2:
            data2 = json.load(file2)
            merged_data.extend(data2)

        with open(output_file, 'w') as out_file:
            json.dump(merged_data, out_file, indent=4)

        print(f"Merged JSON data from {input_file_1} and {input_file_2} saved to {output_file}")
