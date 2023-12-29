import json
import pandas as pd

file_path = "data\\train_permutation_12_trial_3.jsonl"
save_file_path = "data\\train_permutation_12_trial_3_reinstructed.jsonl"
original_length = 7473

dataset= []
with open(file_path, 'r') as f:
    _dataset = f.readlines()
for _data in _dataset:
    dataset.append(json.loads(_data))


original_part = dataset[:original_length]
permutation_part = dataset[original_length:]

for permutation in permutation_part:
    permutation["instruction"] = "Please generate a piece of Prolog code in non-sequential order to solve the given math problem."

original_part = pd.DataFrame(original_part)
permutation_part = pd.DataFrame(permutation_part)

permutation_save = pd.concat([original_part, permutation_part], ignore_index=True)

permutation_save.to_json(save_file_path, orient='records', lines=True)
