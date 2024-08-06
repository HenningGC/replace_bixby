from preprocessor.py import Preprocessor, File
from utils import *
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
import yaml
import os


# TODO: accepts raw data directories from config
def pre_process_datasets():
    with open('config/preprocess_config.yml', 'r') as file:
        config = yaml.safe_load(file)
    # TODO: if config.dataset == value then logic

    for file in os.listdir('data/instruction'):
        
        loaded_file = handler.load_file(file)
        Preprocessor.process_file(file=loaded_file, output_dir='data/instruction', fileProcessor=extract_utterances)




if __name__ == "__main__":
    pre_process_datasets()