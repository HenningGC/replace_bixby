import os
import json
import sys
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv


if 'src/' not in sys.path:
    sys.path.append('src/')

from src.AWSHandler import AWSClientConfig, AWSClient
from src.file_handler import FileHandler


def load_data():
    with open('config/preprocess_config.yml', 'r') as file:
        config = yaml.safe_load(file)

handler = FileHandler()
handler.merge_files(method='merge_two_json_files', input_file_1="data/natural/naturalTrainSet.json", input_file_2= 'data/instruction/instrTrainSet.json', output_file='data/clean_dataset/train_set.json')
handler.merge_files(method='merge_two_json_files', input_file_1="data/natural/naturalDevSet.json", input_file_2= 'data/instruction/instrDevSet.json', output_file='data/clean_dataset/dev_set.json')
handler.merge_files(method='merge_two_json_files', input_file_1="data/natural/naturalTestSet.json", input_file_2= 'data/instruction/instrTestSet.json', output_file='data/clean_dataset/test_set.json')
