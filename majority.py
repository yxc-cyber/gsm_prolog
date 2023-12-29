import os
import json
import functools
from utils import *
from subprocess_prolog_wrapper import get_prolog_result
from threading import Thread
from tqdm import tqdm
from collections import Counter

def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print ('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

@timeout(600)
def get_prolog_result_with_timeout(complete_filename):
    return get_prolog_result(complete_filename)

output_file_path = "data"
output_file_name = ["output_part1.jsonl", "output_part2.jsonl"]
test_file_name = "gsm_prolog_test.jsonl"
K = 100
temperature = 1

with open(os.path.join(output_file_path, output_file_name[0]), 'r') as f:
    data_points0 = f.readlines()

with open(os.path.join(output_file_path, output_file_name[1]), 'r') as f:
    data_points1 = f.readlines()

data_points = data_points0 + data_points1

with open(os.path.join(output_file_path, test_file_name), 'r') as f:
    answer_points = f.readlines()

# assert len(data_points) == len(answer_points)*K

print("Start checking answers.")

maj, total, syntax_correct = 0, 0, 0
for idx in tqdm(range(len(answer_points))):
    if idx*K >= len(data_points):
        continue
    answer_point = json.loads(answer_points[idx])
    answer = answer_point['output']
    with open("temp_answer.pl", 'w') as f:
        f.write(answer)
    answer_result = get_prolog_result_with_timeout("temp_answer.pl")
    output_counter = Counter()
    for output_idx in range(idx*K, (idx+1)*K):
        if output_idx >= len(data_points):
            continue
        data_point = json.loads(data_points[output_idx])
        output = data_point['output']
        with open("temp_output.pl", 'w') as f:
            f.write(output)
        try:
            output_result = get_prolog_result_with_timeout("temp_output.pl")
        except:
            pass
        else:
            if output_result['message'] == NOERROR_CODE:
                output_counter[str(output_result['consult_ans'])] += 1
                syntax_correct += 1
    if len(output_counter.most_common(1)) != 0 and output_counter.most_common(1)[0][0] == answer_result['consult_ans']:
        maj += 1
    total += 1

print(f"The maj1@{K} when temperature is {temperature}: {maj/total}")
print(f"There are {syntax_correct} samples with correct syntax")