from json import dumps
from torch.optim import Adam

from network import CNNNetwork
from deepproblog.network import Network
from deepproblog.model import Model
from deepproblog.engines.exact_engine import ExactEngine
from deepproblog.utils import format_time_precise
from deepproblog.evaluate import get_confusion_matrix
from deepproblog.train import train_model
from deepproblog.dataset import DataLoader
from data.data import SORTOFCLEVRDataset
import random

random.seed(0)
#np.random.seed(args.seed)

width = 6
out_size = (width ** 2) * 2 # Times two for the distinction between squares and circles

colors = ["red", "green", "blue", "orange", "grey", "yellow"]
used_colors = colors[0:width]
cnns = {}
for i, color in enumerate(used_colors):
    cnn = CNNNetwork(out_size=out_size)
    cnns["cnn_" + color] = cnn

nets = {}
nets_ordered = []
for i, color in enumerate(used_colors):
    net = Network(cnns["cnn_" + color], "cnn_" + color, Adam(cnns["cnn_" + color].parameters(), lr=3e-3), batching=True)
    nets["net_" + color] = net
    nets_ordered.append(net)

model = Model("/home/jorrit/Data/KU Leuven/Semester 12/Capita Selecta H05N0a/deepproblog/src/deepproblog/examples/SORTOFCLEVR/model.pl", nets_ordered)

train_dataset = SORTOFCLEVRDataset("train", width)
val_dataset = SORTOFCLEVRDataset("val", width)
test_dataset = SORTOFCLEVRDataset("test", width)
loader = DataLoader(train_dataset, 32, shuffle=True)

model.add_tensor_source("train", train_dataset)
model.add_tensor_source("val", val_dataset)
model.add_tensor_source("test", test_dataset)
model.set_engine(ExactEngine(model), cache=True)
test_accs = []
train_accs = []

train_log = train_model(
    model,
    loader,
    1,
    log_iter=3,
    initial_test=False,
    test_iter=50,
    test=lambda x: [
        #("Val_accuracy", get_confusion_matrix(x, val_dataset, eps=1e-6).accuracy()),
        ("Test_accuracy", get_confusion_matrix(x, test_dataset, eps=1e-6).accuracy()),
        #("Train_accuracy", get_confusion_matrix(x, test_dataset, eps=1e-6).accuracy())
    ],
)

name = "sort_of_clevr_" + format_time_precise()

model.save_state("models/" + name + ".pth")
final_acc = get_confusion_matrix(model, test_dataset, eps=1e-6, verbose=0).accuracy()
train_log.logger.comment("Accuracy {}".format(final_acc))
train_log.logger.comment(dumps(model.get_hyperparameters()))
train_log.write_to_file("log/" + name)
  