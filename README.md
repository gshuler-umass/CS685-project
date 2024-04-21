# CS685-project

most code taken straight from cladder repo

must run DataGen from the DataGen folder

the packages with versions in the requirements.txt file are strict

## How to Run Data Generator

## How to Run LLaMa Fine tuning

2. Create a hugging face account and get a token token
3. Request access to the LLaMa 2 7B model here -> https://huggingface.co/meta-llama/Llama-2-7b-hf
3. pip install 'litgpt[all]'
4. litgpt download --repo_id meta-llama/Llama-2-7b-hf --access_token=[YOUR HF TOKEN]
    - Note that the download is approx 27 GB
5. 
## How to Run LLaMa inference