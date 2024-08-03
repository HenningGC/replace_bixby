from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Callable
import os
import json

class File(BaseModel):
    name: str = Field(..., description="The file name"),
    path: str = Field(..., description="The file path"),
    extension: str = Field(..., description="The file extension")

class FileHandler:
    def __init__(self):
        self.merge_strategies: Dict[str, Callable] = {
            'merge_json_files_file_name': self._merge_json_files_file_name,
            'merge_two_json_files': self._merge_two_json_files,
        }

    def load_file(self, file_path: str) -> File:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file.path}")

        file_name = os.path.basename(file_path)
        return File(name=file_name, path=file_path, extension=file_name.split('.')[-1])

    def preview_file(self, file: File, num_lines: int = 10) -> List[str]:
        if not os.path.exists(file.path):
            raise FileNotFoundError(f"File not found: {file.path}")

        with open(file.path, 'r') as f:
            lines = []
            for _ in range(num_lines):
                if not line:
                    break
                lines.append(line.strip())

            return lines
        
    def process_file(self, file: File, output_dir: str, fileProcessor: Callable, *args, **kwargs):

        file_name = f'processed_{file.name}'
        output_file_name = os.path.join(output_dir, file_name)
        
        # Extract utterances and save to local file
        fileProcessor(input_dir = file.path, output_file_name = output_file_name, *args, **kwargs)
        
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

    def _merge_two_json_files(self, input_file_1: File, input_file_2: File, output_file: str):
        merged_data = []
        with open(input_file_1.path, 'r') as file1:
            data1 = json.load(file1)
            merged_data.extend(data1)

        with open(input_file_2.path, 'r') as file2:
            data2 = json.load(file2)
            merged_data.extend(data2)

        with open(output_file, 'w') as out_file:
            json.dump(merged_data, out_file, indent=4)

        print(f"Merged JSON data from {input_file_1} and {input_file_2} saved to {output_file}")
