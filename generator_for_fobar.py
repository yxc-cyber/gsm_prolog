import openai, backoff, json
from tqdm import tqdm
from utils import *

openai.api_base = ""
openai.api_key = ""

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def generate_messages(examples, target):
    messages = [
        {"role": "system", "content": "You are a helpful, pattern-following assistant that rewrite math questions according to instructions. You will recieve a math question and the answer. And then you need will be asked to set one known value to unkown and raise a new question for it."},
    ]

    for example in examples:
        question = example["input"].strip()
        answer_value = int(example["old_answer"])
        removed_predicate = example["removed_predicate"].strip()
        removed_variable = example["removed_variable"].strip()
        removed_value = int(example["new_answer"])
        new_question = example["new_input"].strip()
        messages.append(
            {"role": "system", "name": "example_user", "content": f"Question:\n{question}\n\nAnswer:\n{answer_value}\n\nNow remove the variable {removed_variable} of value {removed_value} in the predicate {removed_predicate} and obtain the new question:\n"},
        )
        messages.append(
            {"role": "system", "name": "example_assistant", "content": f"{new_question}"},
        )

    question = target["input"].strip()
    answer_value = int(target["old_answer"])
    removed_predicate = target["removed_predicate"].strip()
    removed_variable = target["removed_variable"].strip()
    removed_value = int(target["new_answer"])
    messages.append(
        {"role": "user", "content": f"Question:\n{question}\n\nAnswer:\n{answer_value}\n\nNow remove the variable {removed_variable} of value {removed_value} in the predicate {removed_predicate} and obtain the new question:\n"},
    )

    return messages

if __name__ == "__main__":
        
    with open("fobar_example.txt", 'r') as f:
        fobar_new_inputs = f.readlines()

    with open("data\\train_fobar.jsonl", 'r') as f:
        fobars = f.readlines()

    examples = []
    for idx, new_input in enumerate(fobar_new_inputs):
        fobar_sample = json.loads(fobars[idx])
        fobar_sample["new_input"] = new_input.strip()
        examples.append(fobar_sample)
    

    target = {"id": 5, "instruction": "Please generate a piece of Prolog code to solve the given math problem.", "input": "Mark has a garden with flowers. He planted plants of three different colors in it. Ten of them are yellow, and there are 80% more of those in purple. There are only 25% as many green flowers as there are yellow and purple flowers. How many flowers does Mark have in his garden?", "output": ":- use_module(library(clpq)).\ntotal_plants(35).\nsolve(Yellow_plants) :-\n    {Purple_plants = Yellow_plants * 1.8},\n    {Green_plants = (Yellow_plants + Purple_plants) * 0.25},\n    {Total_plants = Yellow_plants + Purple_plants + Green_plants},\n    total_plants(Total_plants).", "removed_predicate": "plants(mark, yellow, 10)", "removed_variable": "Yellow_plants", "old_answer": 35, "new_answer": "10"}

    messages = generate_messages(examples, target)

    completion = completions_with_backoff(
        model = "gpt-3.5-turbo-16k",
        messages = messages,
    )

    new_question = completion.choices[0].message.content
    
    print(f"Question: {target["input"]}")
    print(f"Answer: {target["old_answer"]}")
    print(f"Removed predicate: {target["removed_predicate"]}")
    print(f"Removed variable: {target["removed_variable"]}")
    print(f"Removed value: {target["new_answer"]}")
    print(f"New question: {new_question}")