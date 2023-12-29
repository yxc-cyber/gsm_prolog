import json, itertools, random, threading, pickle
from tqdm import tqdm
from accuracy import get_prolog_result_with_timeout

file_path = "data\\llama-7b\\gsm_prolog_result\\gsm_prolog_train.jsonl"
target_file_path = "data\\train_permutation.jsonl"
num_workers = 28
random.seed(1)


def prolog_permutate(code, flag):
    code_permutations = []

    code = code.replace(" \n", "\n")
    predicates = [predicate.strip() for predicate in code.split(".\n") if predicate]
    lib, facts, solution = predicates[0], predicates[1:-1], predicates[-1].strip(".")
    solution_lines = [line for line in solution.split("\n") if line]
    solution_head, solution_equations = solution_lines[0], solution_lines[1:]
    solution_equations = "\n".join(solution_equations).split(",\n")
    solution_equations_permutations = []
    for idx, permutation in enumerate(itertools.permutations(solution_equations)):
        if idx == 101:
            break
        if idx != 0:
            solution_equations_permutations.append(permutation)
    solution_equations_permutations = random.sample(solution_equations_permutations, min(10, len(solution_equations_permutations)))
    for solution_equations_permutation in tqdm(solution_equations_permutations, leave=False):
        new_solution_equations = ",\n".join(solution_equations_permutation)
        new_solution_line = solution_head + "\n" + new_solution_equations
        facts_solution = facts + [new_solution_line]
        facts_solution_permutations = []
        for idx, permutation in enumerate(itertools.permutations(facts_solution)):
            if idx == 101:
                break
            if idx != 0:
                facts_solution_permutations.append(permutation)
        facts_solution_permutations = random.sample(facts_solution_permutations, min(10, len(facts_solution_permutations)))
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


with open(file_path, 'r') as f:
    _dataset = f.readlines()
_loaded_dataset = []
for idx, _data_point in enumerate(tqdm(_dataset)):
    data_point = json.loads(_data_point)
    instruction, input, output = data_point["instruction"], data_point["input"], data_point["output"]
    _loaded_dataset.append({"id":idx, "instruction":instruction, "input":input, "output":output})

dataset = []
problem_list = []
def process_thread(_dataset, flag):
    for data_point in tqdm(_dataset, leave=False):
        idx, instruction, input, output = data_point["id"], data_point["instruction"], data_point["input"], data_point["output"]
        output_permutations = prolog_permutate(output, flag)
        for output_permutation in output_permutations:
            dataset.append({"id":idx, "instruction": instruction, "input": input, "output": output_permutation})
        if len(output_permutations) < 5:
            tqdm.write(f"find too few permutations at {idx}: only {len(output_permutations)}")
            problem_list.append(idx)

thread_list = []
step_length = len(_dataset)//num_workers+1
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

with open("problem_list", "wb") as fp:   #Pickling
    pickle.dump(problem_list, fp)