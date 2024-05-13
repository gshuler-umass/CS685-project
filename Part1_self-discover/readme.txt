To execute self_discover scripts:
make sure you have an openAI key loaded as an environment variable.

Make sure you are able to run the original CLadder (Jin et al) code per the instructions on: https://github.com/causalNLP/cladder.  This will produce output in json format.

Run the json_to_csv utility found in the root project of our submission github to convert CLadder's json output to csv (e.g. test-generate-anti.json should be provided to our code as test-generate-anti.csv)

Run "selfdiscover_1_2_3 - subtype.py" replacing the name of the input .csv and a desired output .csv in the code. At this moment no command line options are provided.

NOTE: self discover has many stages of token-intensive prompt orchestration between LLM instances.
Please test with a single sample (adjustable under num_samples in the script) as this may exceed your organization's OPENAI usage limits.