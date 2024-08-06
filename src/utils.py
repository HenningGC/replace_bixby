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

def _merge_json_files_file_name(input_folder: str, output_file: str, common_str: str):
    merged_data = []

    for filename in os.listdir(input_folder):
        if common_str in filename and filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r') as file:
                data = json.load(file)
                merged_data.extend(data)

    with open(output_file, 'w') as out_file:
        json.dump(merged_data, out_file, indent=4)

    print(f"Merged JSON data saved to {output_file}")

def _merge_two_json_files(input_file_1: File, input_file_2: File, output_file: str):
    merged_data = []
    with open(input_file_1.path, 'r') as file1:
        data1 = json.load(file1)
        merged_data.extend(data1)

    with open(input_file_2.path, 'r') as file2:
        data2 = json.load(file2)
        merged_data.extend(data2)

    with open(output_file, 'w') as out_file:
        json.dump(merged_data, out_file, indent=4)

    print(f"Merged JSON data from {input_file_1} and {input_file_2} saved to {output_file}")