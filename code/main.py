import os
from dotenv import load_dotenv
import openai
import time

load_dotenv()


def prompt1(text: str, snippet: str) -> str:
    return f"In the sentence \"{text}\", who does the pronoun in \"{snippet}\" refer to? " \
           f"Output only the name, without a period at the end."


def get_result_gpt(prompt: str, retries=5, base_delay=5) -> str:
    # https://platform.openai.com/docs/api-reference/chat/create?lang=python
    for i in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except openai.error.RateLimitError as err:
            delay = base_delay * (2 ** i)  # exponential backoff
            print(f"Rate limit exceeded. Retrying in {delay} seconds.")
            time.sleep(delay)
    raise Exception(f"Failed after {retries} retries")


def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # print(openai.Model.list())

    # https://commonsensereasoning.org/disambiguation.html
    # https://cs.nyu.edu/~davise/papers/PDPChallenge.xml
    file = open('pdpchallenge.txt', 'r')
    lines = file.readlines()
    file.close()

    output_file = open('output-3-5.txt', 'w')

    i = 0
    n_correct = 0
    n = 0
    start = True
    while i < len(lines):
        line = lines[i].strip()
        i += 1  # we read one line
        if line == '' or line == "SAME TEXT AS PREVIOUS QUESTION":
            start = True
        else:
            if start:
                text = line
                snippet = lines[i].strip().removeprefix("Snippet: ")
                i += 1
                choices = []
                while not lines[i].strip().startswith("Correct Answer: "):
                    choices.append(lines[i].strip())
                    i += 1
                correct_l = lines[i].strip().removeprefix("Correct Answer: ")
                # convert correct answer letter to index
                correct_ans = choices[ord(correct_l) - ord('A')]
                prompt = prompt1(text, snippet)
                guess = get_result_gpt(prompt)

                print(correct_ans == guess)
                output_file.write(f"Correct: {correct_ans}\nGuess: {guess}\n\n")

                n_correct += correct_ans == guess
                n += 1
                start = False

    output_file.write(f"n = {n}\nAccuracy: {n_correct / n}")
    output_file.close()


if __name__ == '__main__':
    main()
