from file_handler.py import FileHandler, File
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
import yaml
import os


# TODO: accepts raw data directories from config
def pre_process_datasets():
    with open('config/preprocess_config.yml', 'r') as file:
        config = yaml.safe_load(file)
    # TODO: if config.dataset == value then logic

    handler = FileHandler()
    for file in os.listdir('data/instruction'):
        
        loaded_file = handler.load_file(file)
        handler.process_file(file=loaded_file, output_dir='data/instruction', fileProcessor=extract_utterances)

    handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrDevSet.json',common_str='d_dialogues')
    handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrTestSet.json',common_str='ts_dialogues')
    handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrTrainSet.json',common_str='_audiodialogues_')






if __name__ == "__main__":
    pre_process_datasets()