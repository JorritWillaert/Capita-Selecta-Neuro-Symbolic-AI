import pickle
import cv2
import matplotlib.pyplot as plt
with open('values_of_training_16_03_2022_13_00_6x6_100_epochs.pk', 'rb') as fp:
    train_loss = pickle.load(fp)
    test_loss = pickle.load(fp)
    epoch_accs = pickle.load(fp)
    times = pickle.load(fp)

epoch_accs.insert(0, 1/8)
del epoch_accs[-1]

fig = plt.figure()
ax=fig.add_subplot(111, label="1")
ax1=fig.add_subplot(111, label="2", frame_on=False)

lns1 = ax.plot(train_loss, color="g", label="Training loss")
lns2 = ax.plot(test_loss, color="r", label="Testing loss")
lns3 = ax1.plot(epoch_accs, color="b", label="Testing accuracy")
#ax1.xlabel("Number of batch iterations")
#ax2.ylabel("Loss")
ax.set_xlabel("Epoch", color="black")
ax.set_ylabel("Loss", color="black")
ax.tick_params(axis='x', colors="black")
ax.tick_params(axis='y', colors="black")

#ax1.xaxis.tick_top()
ax1.yaxis.tick_right()
#ax1.set_xlabel('x label 2', color="C1") 
ax1.set_ylabel('Accuracy', color="b")       
#ax1.xaxis.set_label_position('top') 
ax1.yaxis.set_label_position('right') 
#ax1.tick_params(axis='x', colors="C1")
ax1.tick_params(axis='y', colors="b")


leg = lns1 + lns2 + lns3
labs = [l.get_label() for l in leg]
ax1.legend(leg, labs, loc=0)
plt.savefig("plots/pure_cnn_loss_and_acc_6x6_100_epochs.png")

print("Total training time: " + str(times[-1]))