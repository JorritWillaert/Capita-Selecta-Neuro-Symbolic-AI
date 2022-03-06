from deepproblog.dataset import Dataset

class SORTOFCLEVRDataset(Dataset):
    def __len__(self):
        return len(self.examples)

    def to_query(self, i):
        return self.examples[i].to_query()

    def __init__(self, name, filter):
        self.name = name
        self.expressions = []
        self.lengths = defaultdict(list)
        self.images = set()
        with open(root / "expr_{}.json".format(name)) as f:
            data = json.load(f)
            for d in data:
                expression = Expression(d)
                if filter(expression.length):
                    self.lengths[expression.length].append(expression)
                    # self.lengths[expression.length].append(len(self.expressions))
                    self.expressions.append(expression)
                    self.images.update(expression.labeled_images())