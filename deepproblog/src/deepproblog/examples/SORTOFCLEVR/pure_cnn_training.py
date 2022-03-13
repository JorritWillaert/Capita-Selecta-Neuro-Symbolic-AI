from this import d
from data.pure_cnn_data import Pure_CNN_Data
from network_for_pure_CNN import PureCNN
from torch.utils.data import DataLoader
import torch
from torch import nn, tensor

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")



def accuracy_metric(predictions, expected):
    pred = torch.argmax(predictions, dim=1) # Indices of the max value of all elements -> 0 if "no" has highest probability, 1 if "yes"
    return torch.sum(pred.long() == expected).item()

from torch.nn.modules.activation import Softmax
def train(model, train_dl, val_dl, loss_function, optimizer, epochs=10, accuracy_metric=None):

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
                questions = torch.FloatTensor(questions)
                answer_one_hot = torch.zeros((10)).to(device)
                answer_one_hot[answer] = 1.
                if phase == 'train':
                    outputs = model(img, questions)
                    loss = loss_function(outputs, answer_one_hot.long())
                    train_loss.append(loss)
                    
                    # Backpropagation
                    optimizer.zero_grad() # Needed because backprop accumulates the gradients on subsequent passes
                    loss.backward()       # Backpropagates the prediction loss (gradient of the loss with respect to each parameter)
                    optimizer.step()      # adjust the parameters by the collected gradients from the backward step
                
                else:
                    with torch.no_grad(): # disable grad tracking for faster model evaluation
                        outputs = model(img, questions)
                        loss = loss_function(outputs, answer_one_hot.long())
                        val_loss.append(loss)
                        acc = accuracy_metric(outputs, answer_one_hot) #Use self-defined accuracy metric
                        actual_acc += acc
                    
                actual_loss += loss.item() * dataloader.batch_size
                
                if (step+1) % 500 == 0:
                    m = nn.Softmax(dim=1)
                    print("Output   : " + str(m(outputs)[:,1]))
                    print("Expected : " + str(answer_one_hot))
                    #print(outputs - expected)
                    print("Current step: " + str(step+1) + ", loss: " + str(loss.item()))
                    if phase == 'val':
                         print("Accuracy: " + str(acc))

            # Normalize    
            epoch_loss = actual_loss / len(dataloader.dataset)
            epoch_acc = actual_acc / len(dataloader.dataset)
            
            print("Phase: " + str(phase) + ", epoch loss: " + str(epoch_loss) + ", epoch accuracy: " + str(epoch_acc))
            
        torch.save(model.state_dict(), 'model_12_03_2022_18_30_epoch_' + str(epoch) + '.pt')
    print("Training complete")
    return train_loss, val_loss


network = PureCNN(output_size=10) # Yes, no, square, circle, 1, 2, 3, 4, 5, 6
network.to(device)
train_dataset = Pure_CNN_Data("train", 6)
test_dataset = Pure_CNN_Data("test", 6)
train_loader = DataLoader(train_dataset, 32, shuffle=True)
test_loader = DataLoader(test_dataset, 32, shuffle=True)

loss_function = nn.CrossEntropyLoss()
loss_function.to(device)

optimizer = torch.optim.Adam(network.parameters(), lr = 3e-4)

epochs = 20
train_loss, test_loss = train(network, train_loader, test_loader, loss_function, optimizer, epochs, accuracy_metric)