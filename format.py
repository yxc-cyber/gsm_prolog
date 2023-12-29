import os, json

index = 202
output_file_path = "data"
output_file_name = "output_part1.jsonl"

with open(os.path.join(output_file_path, output_file_name), 'r') as f:
    data_points = f.readlines()

data_point = data_points[index]

data_point = json.loads(data_points[index])
instruction, input, output = data_point['instruction'], data_point['input'], data_point['output']

print(f"instruction:\n{instruction}\n\ninput:\n{input}\n\noutput:\n{output}")