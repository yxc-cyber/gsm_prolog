import json
import pandas as pd

file_path = "data\\train_permutation_12.jsonl"
save_file_path_1 = "data\\train_permutation_11_trial_1.jsonl"
save_file_path_2 = "data\\train_permutation_11_trial_2.jsonl"
original_length = 7473

dataset= []
with open(file_path, 'r') as f:
    _dataset = f.readlines()
for _data in _dataset:
    dataset.append(json.loads(_data))

original_part = dataset[:original_length]
permutation_part = dataset[original_length:]

id2permutation_dict = {}
for data in permutation_part:
    id, instruction, input, output = data["id"], data["instruction"], data["input"], data["output"]
    if id not in id2permutation_dict:
        id2permutation_dict[id] = [{"instruction":instruction, "input":input, "output":output, "id":id}]
    else:
        id2permutation_dict[id].append({"instruction":instruction, "input":input, "output":output, "id":id})

permutation_1 = []
permutation_2 = []
for id, data_list in id2permutation_dict.items():
    if len(data_list) == 1:
        permutation_1.append(data_list[0])
        permutation_2.append(data_list[0])
    else:
        assert len(data_list) == 2
        permutation_1.append(data_list[0])
        permutation_2.append(data_list[1])

original_part = pd.DataFrame(original_part)
permutation_1 = pd.DataFrame(permutation_1)
permutation_2 = pd.DataFrame(permutation_2)

permutation_save_1 = pd.concat([original_part, permutation_1], ignore_index=True)
permutation_save_2 = pd.concat([original_part, permutation_2], ignore_index=True)

permutation_save_1.to_json(save_file_path_1, orient='records', lines=True)
permutation_save_2.to_json(save_file_path_2, orient='records', lines=True)
