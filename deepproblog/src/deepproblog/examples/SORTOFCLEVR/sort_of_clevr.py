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


cnn_red = CNNNetwork(out_size=8)
cnn_green = CNNNetwork(out_size=8)

net_red = Network(cnn_red, "cnn_red", Adam(cnn_red.parameters(), lr=3e-3), batching=True)
net_green = Network(cnn_green, "cnn_green", Adam(cnn_green.parameters(), lr=3e-3), batching=True)

model = Model("/home/jorrit/Data/KU Leuven/Semester 12/Capita Selecta H05N0a/deepproblog/src/deepproblog/examples/SORTOFCLEVR/model.pl", [net_red, net_green])

train_dataset = SORTOFCLEVRDataset("train")
val_dataset = SORTOFCLEVRDataset("val")
test_dataset = SORTOFCLEVRDataset("test")
loader = DataLoader(train_dataset, 32, shuffle=True)

model.add_tensor_source("train", train_dataset)
model.add_tensor_source("val", val_dataset)
model.add_tensor_source("test", test_dataset)
model.set_engine(ExactEngine(model), cache=True)

train_log = train_model(
    model,
    loader,
    1,
    log_iter=2,
    #initial_test=False,
    test_iter=3,
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
  