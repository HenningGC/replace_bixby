from AWSHandler import AWSClientConfig, AWSClient
from utils import extract_utterances
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
import yaml
import os


def load_data():
    with open('config/preprocess_config.yml', 'r') as file:
        config = yaml.safe_load(file)

print(config)
handler = FileHandler()
handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrDevSet.json',common_str='d_dialogues')
handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrTestSet.json',common_str='ts_dialogues')
handler.merge_files(method=config['pre_process_datasets']['instruction_dataset']['merge_method'], input_folder='data/instruction', output_file='data/instrTrainSet.json',common_str='_audiodialogues_')


def read_ndjson(file_path):
    objects = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(0,16256):
            line = lines[i]
            line_val = json.loads(line)
            objects.append(
                {
                    "Utterance": line_val['question_text'],
                    "Instruction": False
                }
            )
    with open('data/natural/naturalTrainSet.json', 'w') as out_file:
        json.dump(objects, out_file, indent=4)

read_ndjson('data/natural/naturalAudio.json')

# accepts raw data directories from config
def load_data():
    pass


if __name__ == "__main__":
    load_data()