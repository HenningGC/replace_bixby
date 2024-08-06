from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Callable
import os
import json

class File(BaseModel):
    name: str = Field(..., description="The file name"),
    path: str = Field(..., description="The file path"),
    extension: str = Field(..., description="The file extension")

class Preprocessor:
    @staticmethod
    def load_file(file_path: str) -> File:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file.path}")

        file_name = os.path.basename(file_path)
        return File(name=file_name, path=file_path, extension=file_name.split('.')[-1])
    @staticmethod
    def preview_file(file: File, num_lines: int = 10) -> List[str]:
        if not os.path.exists(file.path):
            raise FileNotFoundError(f"File not found: {file.path}")

        with open(file.path, 'r') as f:
            lines = []
            for _ in range(num_lines):
                if not line:
                    break
                lines.append(line.strip())

            return lines
    @staticmethod
    def process_file(file: File, output_dir: str, fileProcessor: Callable, *args, **kwargs):

        file_name = f'processed_{file.name}'
        output_file_name = os.path.join(output_dir, file_name)
        
        # Extract utterances and save to local file
        fileProcessor(input_dir = file.path, output_file_name = output_file_name, *args, **kwargs)
        
        print(f"Saved processed file to {output_file_name}")

    @staticmethod
    def merge_files(method: Callable, *args, **kwargs):

        return method(*args, **kwargs)


