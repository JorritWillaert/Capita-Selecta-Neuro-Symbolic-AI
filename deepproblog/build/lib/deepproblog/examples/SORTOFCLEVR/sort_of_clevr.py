from json import dumps
from torch.optim import Adam

from deepproblog.examples.SORTOFCLEVR.network import CNNNetwork
from deepproblog.network import Network
from deepproblog.model import Model
from deepproblog.engines.exact_engine import ExactEngine
from deepproblog.utils import format_time_precise
from deepproblog.evaluate import get_confusion_matrix
from deepproblog.train import train_model
from deepproblog.dataset import DataLoader
from deepproblog.examples.SORTOFCLEVR.data.data import SORTOFCLEVRDataset


cnn_red = CNNNetwork(out_size=8)
cnn_green = CNNNetwork(out_size=8)

net_red = Network(cnn_red, "cnn_red", Adam(cnn_red.parameters(), lr=3e-3), batching=True)
net_green = Network(cnn_green, "cnn_green", Adam(cnn_green.parameters(), lr=3e-3), batching=True)

model = Model("/home/jorrit/Data/KU Leuven/Semester 12/Capita Selecta H05N0a/deepproblog/src/deepproblog/examples/HWF/model.pl", [net_red, net_green])

# model.add_tensor_source("sort_of_clevr", TODO)
model.set_engine(ExactEngine(model), cache=True)

dataset = SORTOFCLEVRDataset("train")
val_dataset = SORTOFCLEVRDataset("val")
test_dataset = SORTOFCLEVRDataset("test")
loader = DataLoader(dataset, 32, shuffle=True)

train_log = train_model(
    model,
    loader,
    50,
    log_iter=50,
    inital_test=False,
    test_iter=100,
    test=lambda x: [
        ("Val_accuracy", get_confusion_matrix(x, val_dataset, eps=1e-6).accuracy()),
        ("Test_accuracy", get_confusion_matrix(x, test_dataset, eps=1e-6).accuracy()),
    ],
)

name = "sort_of_clevr_" + format_time_precise()

model.save_state("models/" + name + ".pth")
final_acc = get_confusion_matrix(model, test_dataset, eps=1e-6, verbose=0).accuracy()
train_log.logger.comment("Accuracy {}".format(final_acc))
train_log.logger.comment(dumps(model.get_hyperparameters()))
train_log.write_to_file("log/" + name)
  