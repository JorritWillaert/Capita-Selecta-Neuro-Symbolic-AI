import pickle
import cv2
import matplotlib.pyplot as plt
with open('log/log_2x2_deepproblog.log', 'r') as f:
    content = f.readlines()

train_loss, accuracy = [], []
for i, row in enumerate(content[3:]):
    info = row.split(',')
    accuracy.append(float(info[1]))
    if i == 0:
        train_loss.append(0.8007569704786874)
    else:
        train_loss.append(float(info[3]))
    time = info[2]
fig = plt.figure()
ax=fig.add_subplot(111, label="1")
ax1=fig.add_subplot(111, label="2", frame_on=False)

lns1 = ax.plot(train_loss, color="g", label="Training loss")
#lns2 = ax.plot(test_loss, color="r", label="Testing loss")
lns3 = ax1.plot(accuracy, color="b", label="Testing accuracy")
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


leg = lns1 + lns3
labs = [l.get_label() for l in leg]
ax1.legend(leg, labs, loc=5)
plt.savefig("plots/deepproblog_2x2.png")

print("Total training time: " + str(time))