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