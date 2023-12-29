import json, pandas as pd

file_path = "data\\train_permutation5.jsonl"
output_file_path = "data\\train_permutation_15.jsonl"
base_file_path = "data\\gsm_prolog_train.jsonl"

with open(file_path, 'r') as f:
    _dataset = f.readlines()
dataset = []
for _data_point in _dataset:
    dataset.append(json.loads(_data_point))

dataset_df = pd.DataFrame(dataset)

# Function to sample 'n' data points from each group
def sample_from_group(group, n=1):
    return group.sample(min(n, len(group)))

# Specify the number of data points to sample from each group
sample_size = 5

# Use groupby and apply to sample data points from each group
sampled_df = dataset_df.groupby('id', group_keys=False).apply(lambda group: sample_from_group(group, n=sample_size))

with open(base_file_path, 'r') as f:
    _dataset = f.readlines()
dataset = []
for _data_point in _dataset:
    dataset.append(json.loads(_data_point))

dataset_df = pd.DataFrame(dataset)
dataset_df["id"] = dataset_df.index

sampled_df = pd.concat([dataset_df, sampled_df], ignore_index=True)

sampled_df.to_json(output_file_path, orient='records', lines=True)