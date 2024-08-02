import os
import json

with open('data/natural/naturalAudio.json','r') as file:
    print(json.load(file)[0])