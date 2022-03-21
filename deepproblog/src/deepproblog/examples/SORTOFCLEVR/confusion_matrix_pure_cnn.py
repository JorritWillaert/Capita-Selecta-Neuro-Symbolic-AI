import torch
from torch.utils.data import DataLoader
from data.pure_cnn_data import Pure_CNN_Data
from network_for_pure_CNN import PureCNN
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

size = 6
output_size = 4 + size
network = PureCNN(size=size, output_size=output_size) # Yes, no, square, circle, 1, 2, 3, 4, 5, 6
train_dataset = Pure_CNN_Data("train", size)
val_dataset = Pure_CNN_Data("val", size)
batch_size = 8
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)

y_pred = []
y_true = []

network.load_state_dict(torch.load("models/model_pure_NN_6x6_100_iterations_16_03_2022.pt"))
network.eval()
# iterate over test data
for (img, questions, answer) in val_loader:
    output = network(img, questions) # Feed Network

    output = torch.argmax(output, dim=1).cpu().numpy()
    y_pred.extend(output) # Save Prediction

    labels = answer.cpu().numpy()
    y_true.extend(labels) # Save Truth

# constant for classes
classes = ('Rectangle', 'Circle', 'Yes', 'No', '1', '2', '3', '4', '5', '6')

# Build confusion matrix
cf_matrix = confusion_matrix(y_true, y_pred)
df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix), index = [i for i in classes],
                     columns = [i for i in classes])
plt.figure(figsize = (12,7))
sn.heatmap(df_cm, annot=True)
plt.savefig('plots/confusion_matrix_6x6_big_testset_iterations.png')