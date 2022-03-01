from torch.optim import Adam

from deepproblog.src.deepproblog.examples.SORT_OF_CLEVR.network import CNNNetwork
from deepproblog.src.deepproblog.network import Network
from deepproblog.src.deepproblog.model import Model

cnn_red = CNNNetwork(out_size=8)
cnn_green = CNNNetwork(out_size=8)

net1 = Network(cnn_red, "cnn_red", Adam(cnn_red.parameters(), lr=3e-3), batching=True)
net2 = Network(cnn_green, "cnn_green", Adam(cnn_green.parameters(), lr=3e-3), batching=True)

model = Model("model.pl", [net1, net2])