from random import weibullvariate
from this import d
from data.pure_cnn_data import Pure_CNN_Data
from network_for_pure_CNN import PureCNN
from torch.utils.data import DataLoader
import torch
from deepproblog.utils import format_time_precise
from torch import nn, tensor

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

def accuracy_metric(predictions, expected):
    print(predictions)
    pred = torch.argmax(predictions, dim=1) # Indices of the max value of all elements -> 0 if "no" has highest probability, 1 if "yes"
    print(pred, expected)
    return torch.sum(pred == expected).item()

from torch.nn.modules.activation import Softmax
def train(model, train_dl, val_dl, loss_function, optimizer, epochs=10, accuracy_metric=None, batch_size=8):

    train_loss, val_loss = [], []
     
    # Optimization loop
    for epoch in range(epochs):
        print('Epoch: ' + str(epoch))

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train(True)
                dataloader = train_dl
            else:
                model.train(False)
                dataloader = val_dl
            
            actual_loss = 0.0
            actual_acc = 0.0
            
            for step, (img, questions, answer) in enumerate(dataloader):
                if phase == 'train':
                    outputs = model(img, questions)
                    loss = loss_function(outputs, answer.long())
                    train_loss.append(loss)
                    
                    # Backpropagation
                    optimizer.zero_grad() # Needed because backprop accumulates the gradients on subsequent passes
                    loss.backward()       # Backpropagates the prediction loss (gradient of the loss with respect to each parameter)
                    optimizer.step()      # adjust the parameters by the collected gradients from the backward step
                
                else:
                    with torch.no_grad(): # disable grad tracking for faster model evaluation
                        outputs = model(img, questions)
                        loss = loss_function(outputs, answer.long())
                        val_loss.append(loss)
                        acc = accuracy_metric(outputs, answer) #Use self-defined accuracy metric
                        actual_acc += acc
                    
                actual_loss += loss.item() * dataloader.batch_size
                
                if (step+1) % 500 == 0:
                    m = nn.Softmax(dim=1)
                    #print("Output   : " + str(outputs))
                    #print("Expected : " + str(answer))
                    #print(outputs - expected)
                    print("Current step: " + str(step+1) + ", loss: " + str(loss.item()))
                    if phase == 'val':
                         print("Accuracy: " + str(acc))

            # Normalize    
            epoch_loss = actual_loss / len(dataloader.dataset)
            epoch_acc = actual_acc / len(dataloader.dataset)
            
            print("Phase: " + str(phase) + ", epoch loss: " + str(epoch_loss) + ", epoch accuracy: " + str(epoch_acc))
    
    name = "sort_of_clevr_" + format_time_precise()
    torch.save(model.state_dict(), 'models/' + name + '.pt')
    print("Training complete")
    return train_loss, val_loss

def init_weights(m):
    if isinstance(m, (nn.Linear, nn.Conv2d)):
        torch.nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.01)
   
size = 2
output_size = 4 + size
network = PureCNN(size=size, output_size=output_size) # Yes, no, square, circle, 1, 2, 3, 4, 5, 6
network.to(device)
train_dataset = Pure_CNN_Data("train", size)
test_dataset = Pure_CNN_Data("test", size)
batch_size = 8
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

for (img, questions, answer) in train_loader:
    network(img, questions)
network.apply(init_weights)

freq_number = 1 / (4 * size)
freqs = [1/8, 1/8, 1/4, 1/4]
for i in range(size):
    freqs.append(freq_number)
freqs = torch.FloatTensor(freqs)
weights = 1 / freqs
print(weights)
weights = weights / torch.sum(weights)
print(weights)
# Chance on shape = 1/4, answer = rectangle or shape. So freq is 1/8
# Chance on horizontal or vertical = 1/2, answer = yes or no. So freq is 1/2
# Chance on number of objects = 1/4, answer = 1, 2, 3, 4, 5 or 6. So freq is 1 / (4 * 6)
loss_function = nn.CrossEntropyLoss(weight=weights)
loss_function.to(device)

optimizer = torch.optim.Adam(network.parameters(), lr = 3e-4)

epochs = 2000
train_loss, test_loss = train(network, train_loader, test_loader, loss_function, optimizer, epochs, accuracy_metric, batch_size)