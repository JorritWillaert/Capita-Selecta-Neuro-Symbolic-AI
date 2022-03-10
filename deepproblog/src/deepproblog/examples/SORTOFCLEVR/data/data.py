import os
import ast
import torchvision.transforms as transforms

from deepproblog.dataset import ImageDataset
from deepproblog.query import Query
from problog.logic import Term, Constant
import random
random.seed(0)

path = os.path.dirname(os.path.abspath(__file__))
num = 2
size = str(num) + 'x' + str(num)

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)

class SORTOFCLEVRDataset(ImageDataset):
    def __init__(
        self,
        subset,
    ):
        super().__init__("{}/{}/{}/images".format(path, size, subset), transform=transform)
        self.data = []
        self.subset = subset
        with open("{}/{}/{}/{}.csv".format(path, size, subset, subset)) as f:
            for line in f:
                norelational_question, norelational_answer, binary_question, binary_answer = \
                    [(l.rstrip('\n')[1:-1]).split() for l in line.split(",")]
                norelational_question = list(map(int, list(map(float, norelational_question))))
                norelational_answer = int(float(norelational_answer[0]))
                binary_question = list(map(int, list(map(float, binary_question))))
                binary_answer = int(float(binary_answer[0]))
                self.data.append((norelational_question, norelational_answer, binary_question, binary_answer))

    def to_query(self, i):
        norelational_question, norelational_answer, binary_question, binary_answer = self.data[i]
        if random.random() < 0.75: # Select nonbinary questions with 75% chance (three questions nonbinary / one question binary)
            sh = None
            for j, color in enumerate(["red", "green", "blue", "orange", "grey", "yellow"]):
                if norelational_question[j] == 1:
                    sh = color
                if j == num - 1:
                    break
            if sh is None:
                print("[ERROR] No object specified")
            
            assert(norelational_question[num] == 1 and norelational_question[num + 1] == 0) # Nonbinary question
            
            question = None
            outcome = None
            if norelational_question[num + 2] == 1: # Query about the shape of the object
                question = "shape"
                if norelational_answer == 2:
                    outcome = 1 #"rectangle"
                elif norelational_answer == 3:
                    outcome = 0 # "circle"
                else:
                    print("[ERROR] Wrong outcome for the shape")
            elif norelational_question[num + 3] == 1: # Query about the horizontal position
                question = "horizontal_side"
                if norelational_answer == 0:
                    outcome = 1 # "left"
                elif norelational_answer == 1:
                    outcome = 0 # "right"
                else: 
                    print("[ERROR] Wrong outcome for the horizontal position")
            elif norelational_question[num + 4] == 1: # Query about the vertical position
                question = "vertical_side"
                if norelational_answer == 0:
                    outcome = 1 # "bottom"
                elif norelational_answer == 1:
                    outcome = 0 # "top"
                else: 
                    print("[ERROR] Wrong outcome for the vertical position")
            else:
                print("[ERROR] No question specified")

        else:
            sh = None
            for j, color in enumerate(["red", "green", "blue", "orange", "grey", "yellow"]):
                if binary_question[j] == 1: 
                    sh = color
                if j == num - 1:
                    break
            if sh is None:
                print("[ERROR] No object specified")
            
            assert(binary_question[num] == 0 and binary_question[num + 1] == 1) # Binary question
            
            assert(binary_question[num + 2] == 0 and binary_question[num + 3] == 0 and binary_question[num + 4] == 1) # Only questions about the number of these shapes of objects are allowed

            question = "number_of_shapes"
            assert(binary_answer >= 4)
            outcome = binary_answer - 3
        sub = {Term("image"): Term("tensor", Term(self.subset, Constant(i)))}
        question = sh + "_" + question
        return Query(Term(question, Term("image"), Constant(outcome)), sub)
           
    def __len__(self):
        return len(self.data)

if __name__ == "__main__":
    train_dataset = SORTOFCLEVRDataset("train")
    test_dataset = SORTOFCLEVRDataset("test")
