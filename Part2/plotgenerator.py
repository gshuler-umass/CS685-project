'''
Code to generate the plot for the Part 2 Bar Graph of the results

NOTE: matplotlib is necessary to run this file
'''
import numpy as np
import matplotlib.pyplot as plt

# results data
results = [
    # random selection
    {"precision": 0.5, "recall": 0.5, "accuracy": 0.5, "model_name": "Random Selection"},
    # llama2
    {"precision": 0.5, "recall": 0.5, "accuracy": 0.5, "model_name": "LLaMa 2 7B Base"},
    # llama3
    {"precision": 0.5, "recall": 0.5, "accuracy": 0.5, "model_name": "LLaMa 3 8B Base"},
    # llama2 QLoRA
    {"precision": 0.5, "recall": 0.5, "accuracy": 0.5, "model_name": "LLaMa 2 7B QLoRA"},
    # llama3 QLoRA
    {"precision": 0.5, "recall": 0.5, "accuracy": 0.5, "model_name": "LLaMa 3 8B QLoRA"},
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
    res_metric = [item[metric] for item in results]
    bar = ax1.bar(indices + temp_width, res_metric, label=metric.capitalize(), width=width)
    temp_width += width


ax1.set_xlabel("Case", fontsize="large", fontweight="semibold", )
ax1.set_ylabel("%", fontweight="semibold",fontsize="large")
ax1.set_title("Precision, Accuracy, and Recall for each Case",fontsize="x-large")
ax1.set_ylim(0, 1)
ax1.set_xticks(indices + width / 3, bins, fontsize="small")
plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment="right")

ax1.legend(metrics, loc="upper right", fancybox=True, shadow=True, ncols=1, bbox_to_anchor=(1,1))

fig1.tight_layout()

# save plot to a file
fig1.savefig("finetuning_barchart.png")
