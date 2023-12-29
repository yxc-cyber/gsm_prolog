import os
import re
from dataset import get_examples, extract_answer
from subprocess_prolog_wrapper import get_prolog_result

targeted_path = 'prolog_files'
examples = get_examples('train')

num = 0
fixed_num = 0
wrong_num = 0
for (root, dirs, files) in os.walk(targeted_path):
    for filename in files:
        if "#" in filename:
            try:
                # complete_filename = os.path.join(root, filename).replace("\\","/")
                # prolog_result = get_prolog_result(complete_filename)
                # assert prolog_result['message'] == 0
                # consult_ans = prolog_result['consult_ans']

                # regex = re.compile(r"(\-?[0-9\.\,]+)#")
                # match = regex.search(filename)
                # idx = int(match.group(1).strip())
                # target_ans = extract_answer(examples[idx]['answer'])

                # if int(consult_ans) == int(target_ans):
                #     os.rename(os.path.join(root, filename), os.path.join(root, f'{idx}.pl'))
                #     print(f"Misclassified sample: {idx}")
                #     num += 1
                #     fixed_num += 1
                # else:
                #     wrong_num += 1
                wrong_num += 1
            except:
                wrong_num += 1
        else:
            num += 1
print(f"Valid samples: {num}, Fixed samples: {fixed_num}, Wrong samples: {wrong_num}")