import torch
from torch.utils.data import Dataset
import os
from pathlib import Path
import torchvision.transforms as transforms
from PIL import Image
import random

path = os.path.dirname(os.path.abspath(__file__))
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)

class Pure_CNN_Data(Dataset):
    def __init__(self, subset, width, extension="png"):
        super().__init__()
        root = "{}/{}/{}/images".format(path, str(width) + 'x' + str(width), subset)
        self.root = Path(root)
        self.transform = transform
        self.extension = extension
        self.subset = subset
        self.data = []
        size = str(width) + 'x' + str(width)
        self.subset = subset
        self.width = width
        with open("{}/{}/{}/{}.csv".format(path, size, subset, subset)) as f:
            for line in f:
                norelational_question, norelational_answer, binary_question, binary_answer = \
                    [(l.rstrip('\n')[1:-1]).split() for l in line.split(",")]
                norelational_question = list(map(int, list(map(float, norelational_question))))
                norelational_answer = int(float(norelational_answer[0]))
                binary_question = list(map(int, list(map(float, binary_question))))
                binary_answer = int(float(binary_answer[0]))
                self.data.append((norelational_question, norelational_answer, binary_question, binary_answer))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if type(idx) is tuple:
            idx = idx[0]
        p = self.root / "{}.{}".format(idx, self.extension)
        with open(p, "rb") as f:
            img = Image.open(f)
            img = img.convert("RGB")
            if self.transform is not None:
                img = self.transform(img)
        norelational_question, norelational_answer, binary_question, binary_answer = self.data[idx]
        if random.random() < 0.75:
            return img, torch.FloatTensor(norelational_question), norelational_answer
        else:
            return img, torch.FloatTensor(binary_question), binary_answer