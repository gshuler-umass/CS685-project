# CS685-project
## How to Run the Self-Discover Prompts
The below instructions assume a Linux environment. The commands will be slightly different for Windows.

1. git clone the project repo at the following link:

   https://github.com/gshuler-umass/CS685-project.git
2. Open a terminal window and navigate to the cladder folder
3. Create a python venv by running the command `python3 -m venv ./venv`
4. Activate the venv with the command `source venv/bin/activate`
5. Run the command `pip install pandas openai`
6. Obtain an OpenAI API key and save it as an environment variable called **OPENAI_API_KEY**
7. Obtain a JSON data file from the CLadder HuggingFace repo
   - https://huggingface.co/datasets/causalnlp/CLadder
8. Convert the JSON data file to the necessary CSV format using the 'json_csv_conv.py' file in the 'json_csv_conv' folder
9. Navigate to the 'self-discover' directory and open the 'selfdiscover_1_2_3 - subtype.py' file. Replace the filenames for the variables 'out_file' and 'in_file' on lines 18 and 19 accordingly. Save and close the file.
10. Run the python file 'selfdiscover_1_2_3 - subtype.py'. The outputted file will be created at the path specified by 'out_file'.
    - Note: It is recommended to test with a single sample first by changing the num_samples variable in the python file first. 

## How to Run the Data Generator
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

## How to Run LLaMa QLoRA

## How to Run LLaMa Inference