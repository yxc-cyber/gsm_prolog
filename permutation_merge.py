import json
import pandas as pd

file_path_1 = "data\\train_permutation_11_trial_1.jsonl"
file_path_2 = "data\\train_permutation_11_trial_3.jsonl"
save_file_path = "data\\train_permutation_12_trial_3.jsonl"
original_length = 7473

dataset_1= []
with open(file_path_1, 'r') as f:
    _dataset_1 = f.readlines()
for _data in _dataset_1:
    dataset_1.append(json.loads(_data))

dataset_2= []
with open(file_path_2, 'r') as f:
    _dataset_2 = f.readlines()
for _data in _dataset_2:
    dataset_2.append(json.loads(_data))

original_part_1 = dataset_1[:original_length]
permutation_part_1 = dataset_1[original_length:]

original_part_2 = dataset_2[:original_length]
permutation_part_2 = dataset_2[original_length:]

id2permutation_dict = {}
for data in permutation_part_1:
    id, instruction, input, output = data["id"], data["instruction"], data["input"], data["output"]
    if id not in id2permutation_dict:
        id2permutation_dict[id] = [{"instruction":instruction, "input":input, "output":output, "id":id}]
    else:
        id2permutation_dict[id].append({"instruction":instruction, "input":input, "output":output, "id":id})
for data in permutation_part_2:
    id, instruction, input, output = data["id"], data["instruction"], data["input"], data["output"]
    if id not in id2permutation_dict:
        id2permutation_dict[id] = [{"instruction":instruction, "input":input, "output":output, "id":id}]
    else:
        if output != id2permutation_dict[id][0]["output"]:
            id2permutation_dict[id].append({"instruction":instruction, "input":input, "output":output, "id":id})

permutation = []
for id, data_list in id2permutation_dict.items():
    if len(data_list) == 1:
        permutation.append(data_list[0])
    else:
        assert len(data_list) == 2
        permutation.append(data_list[0])
        permutation.append(data_list[1])

original_part = pd.DataFrame(original_part_1)
permutation = pd.DataFrame(permutation)

permutation_save = pd.concat([original_part, permutation], ignore_index=True)

permutation_save.to_json(save_file_path, orient='records', lines=True)
