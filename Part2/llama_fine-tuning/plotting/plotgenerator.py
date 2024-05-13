'''
Code to generate the plot for the Part 2 Bar Graph of the results

NOTE: matplotlib is necessary to run this file
'''
import numpy as np
import matplotlib.pyplot as plt

# results data
results = [
    # random selection
    {'model_name': "Random Selection", 'precision': 0.45616883116883117, 'recall': 0.48490077653149266, 'accuracy': 0.48579545454545453, 'f1_score': 0.47009619406106234},
    # llama2
    {"model_name": "LLaMa 2 7B Base", 'precision': 0.4721311475409836, 'recall': 0.993960310612597, 'accuracy': 0.4744318181818182, 'f1_score': 0.6401778271742151},
    # llama3
    {'model_name': "LLaMa 3 8B Base", 'precision': 0.5025510204081632, 'recall': 0.3399482312338223, 'accuracy': 0.53125, 'f1_score': 0.40555841482243954},
    # llama2 QLoRA
    {'model_name': "LLaMa 2 7B QLoRA", 'precision': 0.8995535714285714, 'recall': 0.34771354616048317, 'accuracy': 0.6749188311688312, 'f1_score': 0.5015556938394523},
    # llama3 QLoRA
    {'model_name': "LLaMa 3 8B QLoRA", 'precision': 0.808641975308642, 'recall': 0.7911993097497843, 'accuracy': 0.8137175324675324, 'f1_score': 0.7998255560401222},
    # CLadder
    {"precision": 0, "recall": 0, "accuracy": 0.4466, "model_name": "CLadder"},
]
# setup
width = 0.2
N = len(results)
indices = np.arange(N)
bins = [item["model_name"] for item in results]
metrics = ("precision", "accuracy", "recall")
# define the plot
fig1, ax1 = plt.subplots()


temp_width = width * -2/3
for metric in metrics:
    #plot each metric
    res_metric = [item[metric]*100 for item in results]
    bar = ax1.bar(indices + temp_width, res_metric, label=metric.capitalize(), width=width)
    temp_width += width


ax1.set_xlabel("Case", fontsize="large", fontweight="semibold", )
ax1.set_ylabel("%", fontweight="semibold",fontsize="large")
ax1.set_title("Precision, Accuracy, and Recall for each Case",fontsize="x-large")
ax1.set_xticks(indices + width / 3, bins, fontsize="small")
plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment="right")
ax1.legend(metrics, loc="upper right", fancybox=True, shadow=True, ncols=1, bbox_to_anchor=(1,1))

fig1.tight_layout()

# save plot to a file
fig1.savefig("finetuning_barchart.png")
