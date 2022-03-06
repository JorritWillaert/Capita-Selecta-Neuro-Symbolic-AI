import os
import ast
import torchvision.transforms as transforms

from deepproblog.dataset import ImageDataset
from deepproblog.query import Query
from problog.logic import Term, Constant

path = os.path.dirname(os.path.abspath(__file__))

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)

class Coins(ImageDataset):
    def __init__(
        self,
        subset,
    ):
        super().__init__("{}/{}/images".format(path, subset), transform=transform)
        self.data = []
        self.subset = subset
        with open("{}/{}/{}.csv".format(path, subset, subset)) as f:
            for line in f:
                norelational_question, norelational_answer, binary_question, binary_answer = [(l.rstrip('\n')[1:-1]).split() for l in line.split(",")]
                self.data.append((norelational_question, norelational_answer, binary_question, binary_answer))

    def to_query(self, i):
        norelational_question, norelational_answer, binary_question, binary_answer = self.data[i]
        #sub = {Term("a"): Term("tensor", Term(self.subset, Constant(i)))}
        # if j == 0:
        #     return Term('coin', Constant(j + 1), Term('a'), Term(c1)), sub
        # elif j == 1:
        #     return Term('coin', Constant(j + 1), Term('a'), Term(c2)), sub
        # else:
        #return Query(Term("game", Term("a"), Term(outcome)), sub)

    def __len__(self):
        return len(self.data)


train_dataset = Coins("train")
test_dataset = Coins("test")
