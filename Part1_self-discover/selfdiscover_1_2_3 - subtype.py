
import os
import pandas as pd
import numpy as np
import csv
import openai
from openai import OpenAI
import json
import re

openai_api_key = os.environ.get('OPENAI_API_KEY')

def main():
    # Implements 3 self-discover stages as outlined by Zhou et al: https://arxiv.org/pdf/2402.03620.pdf
    # Our variation consists of pre-selecting the most used frequently modules from the full list of 39 from self-discover paper to save context window and compute 
    # the most-used modules in one batch of our causal reasoning test are then fed through separate instances of gpt-4-0613 as described in each stage
    
    out_file="out_file.csv"
    in_file="data_sampled.csv"
    sd_file="selfdiscover_pruned.txt"
    json_example_file="json_example.txt"    
    num_samples = 30
    sys_prompt = 'I will present you with a logic problem problem and a set of reasoning modules.  Please select only the most relevant modules (1-3 modules total) that would help solve the task.  Only write down numbers corresponding to each reasoning module selected, separated by commas.  No markup or reasoning is required.'
    problem_prompt = ' <PROBLEM:> '
    modules_prompt= ' <REASONING MODULES:> '
    selections_prompt=' <SELECTED MODULES TO ADAPT:>'


    with open(sd_file, 'r') as file:
        sd_text = file.read()
    with open(json_example_file, 'r') as file:
        json_example = file.read()
    client = OpenAI()
    df=pd.read_csv(in_file)
    given_info = df['given_info']
    question = df['question']
    question_id = df['question_id']    
    reasoning = df['reasoning']
    desc_id = df['desc_id']    
    gt = df['answer']
    model_name="gpt-4"#"gpt-4" #"gpt-3.5-turbo","gpt-4-turbo-preview"
    # we randomize the indices so we can sample and filter prompts and gt by these random indices
    indices = np.random.randint(gt.shape[0],size=num_samples)
    question = question[indices]
    gt = gt[indices]
    reasoning = reasoning[indices]
    desc_id = desc_id[indices]
    question_id=question_id[indices]
    given_info=given_info[indices]
    #drop indices
    question.reset_index(drop=True, inplace=True)    
    gt.reset_index(drop=True, inplace=True)
    question_id.reset_index(drop=True, inplace=True)
    reasoning.reset_index(drop=True, inplace=True)
    desc_id.reset_index(drop=True, inplace=True)
    given_info.reset_index(drop=True, inplace=True)
    responses_select =[]

    #STAGE 1 - SELF-DISCOVER: SELECT
    #Where we prompt the model to select reasoning modules for the task at hand


    for n in range(num_samples):
        message = sys_prompt+problem_prompt+given_info[n] + " " +question[n]+modules_prompt+sd_text    

        #api reference https://platform.openai.com/docs/guides/text-generation/chat-completions-api

        response = openai.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a PHD in causal reasoning."},
                {"role": "user", "content": message}
            ]
        )
        responses_select.append(response.choices[0].message.content)


    #STAGE 2 - SELF-DISCOVER: ADAPT
    #Where we prompt the model to adapt the selected modules to be more _specific_ to the task at hand

    sys_prompt = 'I will present you with a logic problem and a set of reasoning modules to adapt to this problem specifically.'
    adapt_prompt= 'Please rewrite only the modules marked to adapt. For example, \"break the problem into subproblems\" becomes \"calculate each arithmetic operation in order for arithmetic problems.\"  Do not offer explanations, just the index number and rewritten adaptation.'


    responses_adapt =[]
    for n in range(num_samples):
        message = sys_prompt+" " + problem_prompt+given_info[n] + " " +question[n]+" "+ modules_prompt + " " + sd_text + adapt_prompt + " " + selections_prompt+" " + responses_select[n] 
        response = openai.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a PHD in causal reasoning."},
                {"role": "user", "content": message}
            ]
        )
        responses_adapt.append(response.choices[0].message.content)

    #STAGE 3 - SELF-DISCOVER: IMPLEMENT
    #Where we prompt the model to create a structured reasoning JSON structure

    sys_prompt = 'I will present you with a logic problem and a set of reasoning modules that you will use to create a json structure to help other models arrive at the correct answer.'
    implement_prompt = 'Here is an example json structure for an unrelated problem to help you structure yours.  Remember, do not include a final answer, just the steps needed. Reply with a single json structure, nothing else, no markup, no explanation or comments'
    responses_implement =[]
    for n in range(num_samples):
        message = sys_prompt+" " + problem_prompt + given_info[n] + " " +question[n] + " " + modules_prompt + " " + sd_text + responses_adapt[n] + " " + implement_prompt+ " " +  json_example
        response = openai.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a PHD in causal reasoning."},
                {"role": "user", "content": message}
            ]
        )
        responses_implement.append(response.choices[0].message.content)


    #FINAL STAGE - SELF-DISCOVER: INFERENCE
    #Inference stage fills in the reasoning JSON structure based on the given information to arrive at a final answer
    responses_infer =[]
    responses_yesno =[]
    sys_prompt = 'I will present you with a logic problem and a json reasoning module that you will follow to arrive at the correct answer.'
    infer_prompt = 'Here is the json structure.  Fill it out step by step including a last field that has a final answer plus one additional one word yes or no brief_final_answer.  no other markup or comments outside the json structure needed.'
    for n in range(num_samples):
        message = sys_prompt+" " + problem_prompt+given_info[n] + " " +question[n] + " " + infer_prompt + " " + responses_implement[n] 
        response = openai.chat.completions.create(
            model=model_name,
            logprobs=False,
            messages=[
                {"role": "system", "content": "You are a PHD in causal reasoning."},
                {"role": "user", "content": message},

            ]

        )
        responses_infer.append(response.choices[0].message.content)

        if ("yes" in response.choices[0].message.content[-15:] or "Yes" in response.choices[0].message.content[-15:]):
                responses_yesno.append("yes")
        if ("no" in response.choices[0].message.content[-15:] or "No" in response.choices[0].message.content[-15:]):
                responses_yesno.append("no")                


    #Pandas df ref https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    responses_infer = pd.Series(responses_infer)    
    responses_adapt = pd.Series(responses_adapt)    
    gt=pd.Series(gt)
    given_info = pd.Series(given_info)
    question = pd.Series(question)
    question_id=pd.Series(question_id)
    reasoning=pd.Series(reasoning)
    desc_id=pd.Series(desc_id)
    responses_select = pd.Series(responses_select) 
    responses_implement = pd.Series(responses_implement)
    responses_yesno = pd.Series(responses_yesno)               
    df_out = pd.DataFrame({'ids':indices, 'desc_id': desc_id, 'original_question_id':question_id, 'given_info':given_info, 'reasoning': reasoning, 'question':question, 'selections': responses_select, 'ground truth':gt, 'adaptations': responses_adapt, 'reasoning structure:': responses_implement, 'answer':responses_infer, 'final_answer':responses_yesno})
    df_out.to_csv(out_file, index=False)


if __name__ == '__main__':
    main()
