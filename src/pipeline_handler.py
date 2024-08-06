from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv, find_dotenv
from typing import List, Callable
import os
import json


class Pipeline:

    def __init__(self, config):

        self.config = config