import json

def extract_utterances(output_file_name):
    with open(output_file_name, 'r') as file:
        data = json.load(file)
        utterances = []
        for item in data:
            turns = item.get('turns',[])
            if not turns:
                return None
            
            utterances.append({
                "Utterance": turns[0].get('utterance', ''),
                "Instruction": True
            })
            

    with open(output_file_name, 'w') as out_file:
        json.dump(utterances, out_file, indent=4)


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