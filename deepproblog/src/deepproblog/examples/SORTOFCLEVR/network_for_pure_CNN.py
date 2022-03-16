from turtle import forward
import torch
from torch import nn
import numpy as np

prob = 0.1
class CNNNetwork(nn.Module):
    def __init__(self, out_size):
        super(CNNNetwork, self).__init__()
        self.convolutions = nn.Sequential(
            nn.Conv2d(3, 6, 5, stride=2),
            nn.ReLU(),
            #nn.BatchNorm2d(6),
            nn.MaxPool2d(2),
            #nn.Conv2d(6, 16, 3, stride=1, padding=1),
            #nn.ReLU(),
            #nn.MaxPool2d(2),
            #nn.Dropout2d(0.4),
        )

        self.mlp = nn.Sequential(
            nn.LazyLinear(out_size),
            #nn.Softmax(dim=1)
            # nn.Dropout2d(0.8)
        )

    def forward(self, x):
        x = self.convolutions(x)
        x = torch.flatten(x, 1)
        x = self.mlp(x)
        return x

class MLP(nn.Module):
    def __init__(self, input_size, out_size): # Input size = (number of colors for one-hot vector of color), 2 for question type (nonbinary VS binary), 3 for question subtype
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            #nn.BatchNorm1d(num_features=16),
            nn.Dropout(prob),
            nn.Linear(16, 8),
            nn.ReLU(),
            #nn.BatchNorm1d(num_features=8),
            nn.Dropout(prob),
            nn.Linear(8, out_size),
            #nn.Softmax(dim=1),
            #nn.ReLU(),
            #nn.BatchNorm1d(num_features=out_size),
            nn.Dropout(prob),
        )

    def forward(self, x):
        return self.net(x)

class Combine(nn.Module):
    def __init__(self, input_size_image, input_size_MLP, out_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size_image + input_size_MLP, 128),
            nn.ReLU(),
            #nn.BatchNorm1d(num_features=128),
            nn.Dropout(prob),
            nn.Linear(128, 32),
            nn.ReLU(),
            #nn.BatchNorm1d(num_features=32),
            nn.Dropout(prob),
            nn.Linear(32, out_size),
            #nn.ReLU(),
            #nn.BatchNorm1d(num_features=out_size),
            nn.Dropout(prob),
        )
    
    def forward(self, x1, x2):
        x3 = torch.cat((x1, x2), dim=1)
        return self.net(x3)

class PureCNN(nn.Module):
    def __init__(self, size, output_size):
        super().__init__()
        self.cnn_net = CNNNetwork(out_size=(size **2) * 2)
        self.mlp = MLP(input_size=size + 2 + 3, out_size=16) # Input size = (number of colors for one-hot vector of color), 2 for question type (nonbinary VS binary), 3 for question subtype
        self.combine = Combine((size **2) * 2, 16, output_size)

    def forward(self, img, question):
        out_cnn = self.cnn_net(img)
        out_mlp = self.mlp(question)
        out_combine =  self.combine(out_cnn, out_mlp)
        return out_combine

if __name__ == "__main__":
    img = torch.ones((1,3,100,100))
    net = CNNNetwork(out_size=4)
    print(net(img))
    print(net)