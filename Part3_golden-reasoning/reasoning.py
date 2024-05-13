import os

import numpy as np
import openai
import pandas as pd

openai_api_key = os.environ.get('OPENAI_API_KEY')


def main():
    out_file = "out_reasoning_file.csv"
    in_file = "data_sampled.csv"

    num_samples = 1

    df = pd.read_csv(in_file)
    given_info = df['given_info']
    question = df['question']
    gt = df['answer']
    reasoning = df['reasoning']
    model_name = "gpt-4"  # "gpt-3.5-turbo","gpt-4-turbo-preview"
    # we randomize the indices so we can sample and filter prompts and gt by these random indices
    indices = np.random.randint(given_info.shape[0], size=num_samples)

    given_info = given_info[indices]
    given_info.reset_index(drop=True, inplace=True)

    question = question[indices]
    question.reset_index(drop=True, inplace=True)

    gt = gt[indices]
    gt.reset_index(drop=True, inplace=True)

    reasoning = reasoning[indices]
    reasoning.reset_index(drop=True, inplace=True)

    example = "We know that high poverty and global water company causes clean water. high poverty or clean water causes cholera contraction. We observed the person is served by a global water company and the region has high poverty. Would the person avoids cholera if clean water instead of polluted water?"
    example_solution = {'step0': 'Let V2 = water company; V1 = poverty; X = water quality; Y = cholera.',
                        'step1': 'V1->X,V2->X,V1->Y,X->Y', 'step2': 'Y_{X=1} = 0 | V2=1, V1=1',
                        'step3': 'Solve for Y, given the evidence and the action',
                        'step4': 'V2 = 1\nV1 = 1\nX = V1 and V2\nY = V1 or X', 'step5': 'Y = 1 = 1 or 1', 'end': '0'}

    # REASONING CHECK - ONE SHOT EXAMPLE
    responses_infer = []

    sys_prompt = 'I will present you with an example logic problem that has a yes or no answer and an example of how to get to an answer through formal reasoning.  Please provide a similar solution for the problem after the example. No other explanation needed'
    for n in range(num_samples):
        message = sys_prompt + " <example problem>" + " " + example + " <example solution>" + str(
            example_solution) + " <new problem>" + given_info[n] + " " + question[n]
        response = openai.chat.completions.create(
            model=model_name,

            messages=[
                {"role": "system", "content": "You are a PHD in causal reasoning."},
                {"role": "user", "content": message},

            ]

        )

        responses_infer.append(response.choices[0].message.content)

    # Pandas df ref https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

    gt = pd.Series(gt)
    given_info = pd.Series(given_info)
    question = pd.Series(question)
    responses_infer = pd.Series(responses_infer)
    reasoning = pd.Series(reasoning)

    df_out = pd.DataFrame(
        {'ids': indices, 'given_info': given_info, 'question': question, 'golden_reasoning': reasoning,
         'ground truth': gt, 'answer': responses_infer})
    df_out.to_csv(out_file, index=False)


if __name__ == '__main__':
    main()
