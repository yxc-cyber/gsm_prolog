import json, pickle, copy
from tqdm import tqdm
from collections import Counter


"""
one
"""

# with open("data\\train_permutation5.jsonl", 'r') as f:
#     perm = f.readlines()
# perm_list = []
# for line in perm:
#     j = json.loads(line)
#     perm_list.append(int(j["id"]))
# perm_counter = Counter(perm_list)

# problem_list = []
# with open("data\\train.jsonl", 'r') as f:
#     train = f.readlines()
# for idx in range(len(train)):
#     if idx not in perm_counter.keys():
#         problem_list.append(idx)

# print(len(problem_list))
# print(problem_list)

# for key, value in perm_counter.items():
#     if value < 5:
#         problem_list.append(key)

# print(len(problem_list))

# with open("problem_list_part5", "wb") as fp:   #Pickling
#     pickle.dump(problem_list, fp)

"""
two
"""

with open("problem_list_part5", 'rb') as fp:
    problem_list = pickle.load(fp)

print("Number of problems:", len(problem_list))

with open("data\\gsm_prolog_train.jsonl", 'r') as f:
    _dataset = f.readlines()

_loaded_dataset = []
for idx, _data_point in enumerate(_dataset):
    data_point = json.loads(_data_point)
    instruction, input, output = data_point["instruction"], data_point["input"], data_point["output"]
    _loaded_dataset.append({"id":idx, "instruction":instruction, "input":input, "output":output})
# _loaded_dataset = [_loaded_dataset[idx] for idx in problem_list]

# print(problem_list[1])
print(_loaded_dataset[problem_list[5]]["output"])

"""
three
"""

# with open("data\\train_permutation4.jsonl", 'r') as f:
#     part1 = f.readlines()
# part1_list = []
# for line in part1:
#     part1_list.append(json.loads(line))
# dataset = copy.deepcopy(part1_list)


# with open("data\\train_permutation_part5.jsonl", 'r') as f:
#     part2 = f.readlines()
# part2_list = []
# for line in part2:
#     part2_list.append(json.loads(line))

# start_idx = 0
# for line_part2 in tqdm(part2_list):
#     flag = 0
#     while start_idx < len(part1_list) and part1_list[start_idx]["id"] <= line_part2["id"]:
#         if part1_list[start_idx]["id"] == line_part2["id"] and part1_list[start_idx]["output"] == line_part2["output"]:
#             flag = 1
#         start_idx += 1
#     if flag == 0:
#         dataset.append(line_part2)

# dataset = sorted(dataset, key=lambda x:x["id"])

# with open("data\\train_permutation5.jsonl", 'w') as f:
#     for data_point in dataset:
#         json.dump(data_point, f)
#         f.write('\n')