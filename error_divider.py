import json

accuracy_file = "F:\S23 DURF\data\llama-2-7b-r32\gsm_prolog_permute_11_trial_3_reinstructed_result\gsm_prolog_permute_11_trial_3_reinstructed_accuracy.json"

with open(accuracy_file, 'r') as f:
    accuracy_record = json.loads(f.read())

SEMANTIC_counter = 0
SYNTAX_counter = 0
for idx, record in accuracy_record["error_idx"].items():
    if record["error_type"] == "SEMANTIC":
        SEMANTIC_counter += 1
    else:
        SYNTAX_counter += 1

total = accuracy_record["total_sample"]

print(f"The syntax error is {SYNTAX_counter/total}")
print(f"The semantic error is {SEMANTIC_counter/total}")