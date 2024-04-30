# CS685-project

## How to Run Data Generator
The below instructions assume a Linux environment. The commands will be slightly different for Windows.
1. git clone the project repo at the following link:

   https://github.com/gshuler-umass/CS685-project.git
2. git clone the cladder project repo at the following link:

   https://github.com/causalNLP/cladder.git
3. Open a terminal window and navigate to the cladder folder
4. Create a python venv by running the command `python3 -m venv ./venv`
5. Activate the venv with the command `source venv/bin/activate`
6. Run `pip install -r requirements.txt` to install the python packages specified in cladder's requirements.txt file
7. Copy the following files from the CS685-project repo to the cladder repo
   - 10 nonsenseX.yml files in the directory Part2/DataGen/assets/stories/ to the directory assets/stories
   - Part2/DataGen/config/proj.yml to config
   - Part2/DataGen/config/stories/proj.yml to config/stories
   - Part2/DataGen/config/queries/proj_queries.yml to config/queries
8. In config/proj.yml
   - specify the path and name of the output JSON (ex: data/proj.json)
   - specify the spec-limit (a spec-limit of 1 generates roughly 1,000 prompts, a spec-limit of 10 generates roughly 10,000 prompts)
9. Finally, to run the data generator run the following command in the terminal from the top level directory of the cladder repo
```
fig generate proj
```
10. The data file will be outputted at the path specified in Step 8. Additionally details of the data will be printed in the terminal

## How to Run LLaMa Fine tuning

2. Create a hugging face account and get a token
3. Request access to the LLaMa 2 7B model here -> https://huggingface.co/meta-llama/Llama-2-7b-hf
3. pip install 'litgpt[all]'
4. litgpt download --repo_id meta-llama/Llama-2-7b-hf --access_token=[YOUR HF TOKEN]
    - Note that the download is approx 27 GB
5. run
```
litgpt finetune lora --data JSON --data.json_path data/proj_data.json --checkpoint_dir checkpoints/meta-llama/Llama-2-7b-hf --out_dir data/proj_data-finetuned
```
## How to Run LLaMa inference