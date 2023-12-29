import json
from dataset import get_examples


split = "train"

target_path = 'prolog_files' if split == 'train' else 'prolog_test_files'

sample_amount = 7473 if split == 'train' else 1319

examples = get_examples(split)

with open('data\\gsm_prolog_train.jsonl', 'w') as outfile:
    for idx in range(sample_amount):
        instruction = 'Please generate a piece of Prolog code to solve the given math problem.'
        question = examples[idx]['question'].strip()
        answer = examples[idx]['answer'].strip()
        with open(f'{target_path}/{idx}.pl', 'r') as prolog_file:
            prolog_code = prolog_file.read().strip()
        sample = {"instruction": instruction, "input": question, "output": prolog_code}
        json.dump(sample, outfile)
        outfile.write('\n')

# with open(f'data/train.jsonl', 'w') as outfile:
#     for idx in range(sample_amount):
#         instruction = 'Please generate a piece of Prolog code to solve the given math problem.'
#         question = examples[idx]['question'].strip()
#         answer = examples[idx]['answer'].strip()
#         sample = {"instruction": instruction, "input": question, "output": answer}
#         json.dump(sample, outfile)
#         outfile.write('\n')