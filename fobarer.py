import json, random, threading, re
from tqdm import tqdm
from accuracy import get_prolog_result_with_timeout
from utils import NOERROR_CODE

file_path = "data\\gsm_prolog_train.jsonl"
target_file_path = "data\\train_fobar.jsonl"
num_workers = 28
random.seed(1)

# file_path = "data\\gsm_prolog_train.jsonl"
# target_file_path = "data\\train_fobar_temp.jsonl"
# num_workers = 1

def parse_fact(fact):
    parse_results = re.compile(r"(\w+)\((.*)\)", re.DOTALL).search(fact)
    if parse_results is not None:
        predicate = parse_results.group(1).strip()
        entries = parse_results.group(2).strip().split(",")
        return predicate, entries
    else:
        return None, None


def prolog_fobar(code, flag):
    code_fobars = []
    errors = []

    code = code.replace(" \n", "\n")
    predicates = [predicate.strip() for predicate in code.split(".\n") if predicate]
    lib, facts, solution = predicates[0], predicates[1:-1], predicates[-1].strip(".")
    facts_and_solution = facts + [solution]
    removal_list = []
    for line in facts_and_solution:
        if line.strip()[0] == "%":
            removal_list.append(line)
        if line[:5] == "solve":
            solution = line
    for line in removal_list:
        facts_and_solution.remove(line)
    facts_and_solution.remove(solution)
    facts = facts_and_solution
    solution_lines = [line for line in solution.split("\n") if line]
    solution_lines_removal = []
    for solution_line_idx, solution_line in enumerate(solution_lines):
        if len(solution_line.strip()) == 0 or solution_line.strip()[0] == "%":
            solution_lines_removal.append(solution_line)
        else:
            if solution_line.find("%") != -1:
                solution_lines[solution_line_idx] = solution_line[: solution_line.find("%")]
    for solution_line in solution_lines_removal:
        solution_lines.remove(solution_line)
    solution_head, solution_equations = solution_lines[0], solution_lines[1:]
    solution_equations = "\n".join(solution_equations).split(",\n")

    for equation_idx, solution_equation in enumerate(solution_equations):
        if solution_equation[:4] != "    ":
            solution_equation = "  " + solution_equation
        if " is " in solution_equation and " // " not in solution_equation:
            solution_equation = solution_equation.replace(" is ", " = ").replace("    ", "    {") + "}"
            solution_equations[equation_idx] = solution_equation

    with open(f"temp_answer{flag}.pl", 'w') as f:
        f.write(code)
    answer_result = get_prolog_result_with_timeout(f"temp_answer{flag}.pl")
    if answer_result["message"] == NOERROR_CODE:
        answer_result = answer_result["consult_ans"]
    else:
        errors.append({"output": None, "removed_predicate": None, "old_answer": None, "new_answer": None, "old_code": code})
        return code_fobars, errors
    old_query_variable = re.compile(r"\((.*)\)", re.DOTALL).search(solution_head).group(1)

    for fact in facts:
        new_solution_head = solution_head
        new_answer_result = None
        new_code = None

        try:
            predicate, entries = parse_fact(fact)
            num_entry_indicies = [idx for idx in range(len(entries)) if (entries[idx].strip().isnumeric() or " / " in entries[idx] or "." in entries[idx] or entries[idx].strip()[0].isupper())]
            new_entries = entries.copy()
            for num_entry_idx in num_entry_indicies:
                new_entries[num_entry_idx] = "(.*)"
            for new_entry_idx, new_entry in enumerate(new_entries):
                if new_entry[0] == " ":
                    new_entries[new_entry_idx] = f" ({new_entry[1:]}|_)"
                else:
                    new_entries[new_entry_idx] = f"({new_entry}|_)"
            template = rf"{predicate}\({",".join(new_entries)}\)"
            for solution_equation in solution_equations:
                new_query_variable_match = re.compile(template, re.DOTALL).search(solution_equation)
                if new_query_variable_match is not None:
                    _, solution_equation_entries = parse_fact(solution_equation)
                    val_entry_indicies = [idx for idx in range(len(solution_equation_entries)) if solution_equation_entries[idx].strip()[0].isupper()]
                    for val_entry_idx in val_entry_indicies:
                        new_solution_equations = solution_equations.copy()
                        new_solution_equations.remove(solution_equation)
                        new_facts = facts.copy()
                        new_facts.remove(fact)
                        new_answer_result = entries[val_entry_idx].strip()
                        new_query_variable = solution_equation_entries[val_entry_idx].strip()
                        new_solution_head = f"solve({new_query_variable}) :-"

                        if " / 100" in new_answer_result:
                            new_answer_result = new_answer_result.strip()[1:-7]
                            for solution_equation_idx, solution_equation in enumerate(new_solution_equations):
                                if new_query_variable in solution_equation:
                                    new_solution_equations[solution_equation_idx] = solution_equation.replace(new_query_variable, f"({new_query_variable} / 100)")

                        new_val_entry_indicies = val_entry_indicies.copy()
                        new_val_entry_indicies.remove(val_entry_idx)
                        for new_val_entry_idx in new_val_entry_indicies:
                            new_val_predicate, new_val_value = solution_equation_entries[new_val_entry_idx], entries[new_val_entry_idx]
                            new_facts.append(f"{new_val_predicate.strip().lower()}({new_val_value.strip()})")
                            new_solution_equations.append(f"    {new_val_predicate.strip().lower()}({new_val_predicate.strip()})")

                        new_facts.append(f"{old_query_variable.strip().lower()}({answer_result})")
                        new_solution_equations.append(f"    {old_query_variable.strip().lower()}({old_query_variable})")
                        new_code = lib + ".\n" + ".\n".join(new_facts) + ".\n" + new_solution_head + "\n" + ",\n".join(new_solution_equations) + "."

                        with open(f"temp_output{flag}.pl", 'w') as f:
                            f.write(new_code)

                        new_output_result = get_prolog_result_with_timeout(f"temp_output{flag}.pl")["consult_ans"]
                        if int(new_output_result) == int(new_answer_result):
                            code_fobars.append({"output": new_code, "removed_predicate": fact, "removed_variable":new_query_variable, "old_answer": answer_result, "new_answer": new_answer_result})
                        else:
                            errors.append({"output": new_code, "removed_predicate": fact, "old_answer": answer_result, "new_answer": new_answer_result, "old_code": code})
        except:
            errors.append({"output": new_code, "removed_predicate": fact, "old_answer": answer_result, "new_answer": new_answer_result, "old_code": code})

    return code_fobars, errors


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
        output_fobars, errors = prolog_fobar(output, flag)
        for output_fobar in output_fobars:
            dataset.append({"id":idx, "instruction": instruction, "input": input, "output": output_fobar["output"], "removed_predicate": output_fobar["removed_predicate"], "removed_variable": output_fobar["removed_variable"], "old_answer": output_fobar["old_answer"], "new_answer": output_fobar["new_answer"]})
        for error in errors:
            problem_list.append({"id":idx, "instruction": instruction, "input": input, "output": error["output"], "removed_predicate": error["removed_predicate"], "old_answer": error["old_answer"], "new_answer": error["new_answer"], "old_code": error["old_code"]})


thread_list = []
step_length = len(_dataset)//num_workers+1
for i in range(num_workers):
    t = threading.Thread(target=process_thread, args=(_loaded_dataset[i*step_length:(i+1)*step_length],i))
    thread_list.append(t)
    t.start()
for t in thread_list:
    t.join()

dataset = sorted(dataset, key=lambda x:x["id"])
problem_list = sorted(problem_list, key=lambda x:x["id"])

with open(target_file_path, 'w') as f:
    for data_point in dataset:
        json.dump(data_point, f)
        f.write('\n')

with open("problem_list.jsonl", 'w') as f:
    for problem_point in problem_list:
        json.dump(problem_point, f)
        f.write('\n')