from AWSHandler import AWSClientConfig, AWSClient
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
import yaml
import os


def preprocess_data():
    with open('config/preprocess_config.yml', 'r') as file:
    config = yaml.safe_load(file)

print(config)
handler = FileHandler()
handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrDevSet.json',common_str='d_dialogues')
handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrTestSet.json',common_str='ts_dialogues')
handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrTrainSet.json',common_str='_audiodialogues_')



if __name__ == "__main__":
    preprocess_data()