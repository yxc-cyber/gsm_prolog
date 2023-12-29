import pickle, json, itertools, random, threading
from tqdm import tqdm
from accuracy import get_prolog_result_with_timeout

file_path = "data\\llama-7b\\gsm_prolog_result\\gsm_prolog_train.jsonl"
target_file_path = "data\\train_permutation_part4.jsonl"
num_workers = 28

def prolog_permutate(code, flag):
    code_permutations = []

    code = code.replace(" \n", "\n")
    predicates = [predicate.strip() for predicate in code.split(".\n") if predicate]
    lib, facts, solution = predicates[0], predicates[1:-1], predicates[-1].strip(".")
    facts_solution = facts + [solution]
    facts_solution_permutations = []
    for idx, permutation in enumerate(itertools.permutations(facts_solution)):
        if idx == 10001:
            break
        if idx != 0:
            facts_solution_permutations.append(permutation)
    facts_solution_permutations = random.sample(facts_solution_permutations, min(10000, len(facts_solution_permutations)))
    for facts_solution_permutation in tqdm(facts_solution_permutations, leave=False):
        new_facts_solution = ".\n".join(facts_solution_permutation)
        new_code = lib + ".\n" + new_facts_solution + "."
        with open(f"temp_output{flag}.pl", 'w') as f:
            f.write(new_code)
        with open(f"temp_answer{flag}.pl", 'w') as f:
            f.write(code)
        try:
            output_result = get_prolog_result_with_timeout(f"temp_output{flag}.pl")
            answer_result = get_prolog_result_with_timeout(f"temp_answer{flag}.pl")
            if output_result == answer_result:
                code_permutations.append(new_code)
        except:
            pass

    return code_permutations


with open("problem_list_part3", 'rb') as fp:
    problem_list = pickle.load(fp)

print("Number of problems:", len(problem_list))

with open(file_path, 'r') as f:
    _dataset = f.readlines()

_loaded_dataset = []
for idx, _data_point in enumerate(_dataset):
    data_point = json.loads(_data_point)
    instruction, input, output = data_point["instruction"], data_point["input"], data_point["output"]
    _loaded_dataset.append({"id":idx, "instruction":instruction, "input":input, "output":output})
_loaded_dataset = [_loaded_dataset[idx] for idx in problem_list]

dataset = []
new_problem_list = []
def process_thread(_dataset, flag):
    for data_point in tqdm(_dataset, leave=False):
        idx, instruction, input, output = data_point["id"], data_point["instruction"], data_point["input"], data_point["output"]
        output_permutations = prolog_permutate(output, flag)
        for output_permutation in output_permutations:
            dataset.append({"id":idx, "instruction": instruction, "input": input, "output": output_permutation})
        if len(output_permutations) < 5:
            tqdm.write(f"find too few permutations at {idx}: only {len(output_permutations)}")
            new_problem_list.append(idx)

# print(problem_list[0])
# print(_loaded_dataset[problem_list[3]]["output"])

thread_list = []
step_length = len(_loaded_dataset)//num_workers+1
for i in range(num_workers):
    t = threading.Thread(target=process_thread, args=(_loaded_dataset[i*step_length:(i+1)*step_length],i))
    thread_list.append(t)
    t.start()
for t in thread_list:
    t.join()

dataset = sorted(dataset, key=lambda x:x["id"])

with open(target_file_path, 'w') as f:
    for data_point in dataset:
        json.dump(data_point, f)
        f.write('\n')

with open("problem_list_part4", "wb") as fp:   #Pickling
    pickle.dump(new_problem_list, fp)