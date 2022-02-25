from torch.optim import Adam

from deepproblog.src.deepproblog.examples.SORT_OF_CLEVR.network import CNNNetwork
from deepproblog.src.deepproblog.model import Model
from deepproblog.src.deepproblog.network import Network

cnn1 = CNNNetwork(out_size=4)
cnn2 = CNNNetwork(out_size=4)
cnn3 = CNNNetwork(out_size=4)
cnn4 = CNNNetwork(out_size=4)

net1 = Network(cnn1, "cnn1", Adam(cnn1.parameters(), lr=3e-3), batching=True)
net2 = Network(cnn2, "cnn2", Adam(cnn2.parameters(), lr=3e-3), batching=True)
net3 = Network(cnn3, "cnn3", Adam(cnn3.parameters(), lr=3e-3), batching=True)
net4 = Network(cnn4, "cnn4", Adam(cnn4.parameters(), lr=3e-3), batching=True)

# Note: maybe I could use four times the same network?

model = Model("model.pl", [net1, net2, net3, net4])