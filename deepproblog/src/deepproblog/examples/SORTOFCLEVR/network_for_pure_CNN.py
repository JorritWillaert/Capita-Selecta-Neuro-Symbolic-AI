from turtle import forward
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

class MLP(nn.Module):
    def __init__(self, input_size, out_size): # Input size = (number of colors for one-hot vector of color), 2 for question type (nonbinary VS binary), 3 for question subtype
        super().__init__()
        self.layer1 = nn.Linear(input_size, 16)
        self.layer2 = nn.Linear(16, 8)
        self.layer3 = nn.Linear(8, out_size)

    def forward(self, x):
        y = self.layer1(x)
        z = self.layer2(y)
        q = self.layer3(z)
        return q

class Combine(nn.Module):
    def __init__(self, input_size_image, input_size_MLP, out_size):
        super().__init__()
        self.layer1 = nn.Linear(input_size_image + input_size_MLP, 128)
        self.layer2 = nn.Linear(128, 32)
        self.layer3 = nn.Linear(32, out_size)
    
    def forward(self, x1, x2):
        y = torch.cat((x1, x2), dim=1)
        z = self.layer1(y)
        q = self.layer2(z)
        r = self.layer3(q)
        return r

class PureCNN(nn.Module):
    def __init__(self, output_size):
        super().__init__()
        self.cnn_net = CNNNetwork(out_size=(6 **2) * 2)
        self.mlp = MLP(input_size=6 + 2 + 3, out_size=16) # Input size = (number of colors for one-hot vector of color), 2 for question type (nonbinary VS binary), 3 for question subtype
        self.combine = Combine((6 **2) * 2, 16, output_size)

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