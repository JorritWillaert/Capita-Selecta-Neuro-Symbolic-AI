import torch
from torch import nn
import numpy as np

class CNNNetwork(nn.Module):
    def __init__(self, out_size):
        super(CNNNetwork, self).__init__()
        self.convolutions = nn.Sequential(
            nn.Conv2d(3, 6, 5, stride=2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            #nn.Conv2d(6, 16, 3, stride=1, padding=1),
            #nn.ReLU(),
            #nn.MaxPool2d(2),
            nn.Dropout2d(0.4),
        )

        self.mlp = nn.Sequential(
            nn.LazyLinear(out_size), # Square and red, square and green, circle and red, circle and green
            nn.Softmax(dim=1)
            # nn.Dropout2d(0.8)
        )

    def forward(self, x):
        x = self.convolutions(x)
        x = torch.flatten(x, 1)
        x = self.mlp(x)
        return x

if __name__ == "__main__":
    img = torch.ones((1,3,100,100))
    net = CNNNetwork(out_size=4)
    print(net(img))
    print(net)