import json, os
from collections import Counter

with open("data\\train_fobar.jsonl", 'r') as f:
    content = f.readlines()
example = json.loads(content[10])
# print("=====old=====")
# print(example["old_code"])
print("=====new=====")
print(example["output"])


# with open("data\\train_fobar.jsonl", 'r') as f:
#     content = f.readlines()
# counter = Counter()
# for c in content:
#     c = json.loads(c)
#     idx = c["id"]
#     counter[idx] += 1
# cc = 0
# for i in range(7473):
#     if counter[i] <= 0:
#         os.system(f"copy .\\prolog_files\\{i}.pl .\\error_files\\{i}.pl")
#         cc += 1
# print(f"Total: {cc}")


# with open("data\\train_fobar.jsonl", 'r') as f:
#     content = f.readlines()
# counter = Counter()
# for c in content:
#     c = json.loads(c)
#     counter[c["id"]] += 1
# cc = Counter()
# for i in range(7473):
#     cc[counter[i]] += 1
# cc = sorted(cc.items(), key=lambda x: x[1], reverse=True)
# print(cc)


# with open("data\\train_fobar.jsonl", 'r') as f:
#     content = f.readlines()
# example = json.loads(content[9])
# print(example["input"])
# print(f"Answer: {example["old_answer"]}")
# print(f"Removed predicate: {example["removed_predicate"]}")
# print(f"Removed variable: {example["removed_variable"]}")
# print(f"Removed value: {example["new_answer"]}")