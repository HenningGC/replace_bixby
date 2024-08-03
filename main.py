import os
import json
import sys
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv


if 'src/' not in sys.path:
    sys.path.append('src/')

from src.AWSHandler import AWSClientConfig, AWSClient
from src.file_handler import FileHandler