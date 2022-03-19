from network import CNNNetwork
from deepproblog.network import Network
from deepproblog.model import Model
from torch.optim import Adam
from deepproblog.dataset import DataLoader
from data.data import SORTOFCLEVRDataset
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from deepproblog.engines.exact_engine import ExactEngine

width = 6
out_size = (width ** 2) * 2 # Times two for the distinction between squares and circles

colors = ["red", "green", "blue", "orange", "grey", "yellow"]
used_colors = colors[0:width]
cnns = {}
for color in colors:
    cnn = CNNNetwork(out_size=out_size)
    cnns["cnn_" + color] = cnn

nets = {}
nets_ordered = []
for color in colors:
    net = Network(cnns["cnn_" + color], "cnn_" + color, Adam(cnns["cnn_" + color].parameters(), lr=3e-3), batching=True)
    nets["net_" + color] = net
    nets_ordered.append(net)


train_dataset = SORTOFCLEVRDataset("train", width)
val_dataset = SORTOFCLEVRDataset("val", width)
test_dataset = SORTOFCLEVRDataset("test", width)
loader = DataLoader(train_dataset, 32, shuffle=True)
test_loader = DataLoader(train_dataset, 32, shuffle=True)

model = Model("/home/jorrit/Data/KU Leuven/Semester 12/Capita Selecta H05N0a/deepproblog/src/deepproblog/examples/SORTOFCLEVR/model.pl", nets_ordered)
model.load_state("models/model_deepproblog_6x6_18_03_2022.pth")
model.add_tensor_source("train", train_dataset)
model.add_tensor_source("val", val_dataset)
model.add_tensor_source("test", test_dataset)
model.set_engine(ExactEngine(model), cache=True)
model.eval()

y_pred, y_true = [], []
for i, gt_query in enumerate(val_dataset.to_queries()):
    val_query = gt_query.variable_output()
    answer = model.solve([val_query])[0]
    if len(answer.result) == 0:
        print("no answer for query {}".format(gt_query))
    else:
        max_ans = max(answer.result, key=lambda x: answer.result[x])
    p = answer.result[max_ans]
    predicted = int(max_ans.args[gt_query.output_ind[0]])
    actual = int(gt_query.output_values()[0])
    question = str(val_query)[6:]
    if question.startswith("horizontal") or question.startswith("vertical"):
        new_predicted = predicted + 2
        new_actual = actual + 2
    elif question.startswith("shape"):
        new_predicted = predicted
        new_actual = actual
    else:
        new_predicted = predicted + 4
        new_actual = actual + 4

    y_pred.append(new_predicted) # Save Prediction
    y_true.append(new_actual) # Save Truth

# constant for classes
classes = ('Rectangle', 'Circle', 'Yes', 'No', '1', '2', '3', '4', '5', '6')

# Build confusion matrix
cf_matrix = confusion_matrix(y_true, y_pred)
df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix), index = [i for i in classes],
                     columns = [i for i in classes])
plt.figure(figsize = (12,7))
sn.heatmap(df_cm, annot=True)
plt.savefig('plots/deepproblog_6x6_18_03_2022_10000_testsize.png')