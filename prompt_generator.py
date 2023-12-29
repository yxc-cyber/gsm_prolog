from dataset import get_examples

examples = get_examples('train')

def generate(questions, target):
    with open('prompt.txt', 'w') as prompt_file:
        for idx in questions:
            question = examples[idx]['question'].strip()
            answer = examples[idx]['answer'].strip()
            with open(f'prolog_files/{idx}.pl', 'r') as prolog_file:
                prolog_code = prolog_file.read().strip()
            prompt_file.write(f'Question:\n{question}\n\n\nAnswer:\n{answer}\n\n\nProlog Code:\n{prolog_code}\n\n\n')
        target_question = examples[target]['question'].strip()
        target_answer = examples[target]['answer'].strip()
        prompt_file.write(f'Question:\n{target_question}\n\n\nAnswer:\n{target_answer}\n\n\nProlog Code:')

if __name__=='__main__':
    target = 5
    generate([0,1,2,3,4], target)