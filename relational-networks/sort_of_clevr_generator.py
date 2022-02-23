from tokenize import String
from turtle import pos, width
import cv2
import os
from matplotlib.widgets import Widget
import numpy as np
import random
#import cPickle as pickle
import pickle
import warnings
import argparse

parser = argparse.ArgumentParser(description='Sort-of-CLEVR dataset generator')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--t-subtype', type=int, default=-1,
                    help='Force ternary questions to be of a given type')
args = parser.parse_args()

#random.seed(args.seed)
#np.random.seed(args.seed)

IMG_SIZE = 100
NUM_OBJECTS = 2
WIDTH = 2

colors = [
    (0,0,255),##r
    (0,255,0),##g
    #(255,0,0),##b
    #(0,156,255),##o
    #(128,128,128),##k
    #(0,255,255)##y
]

class Object: 
    def __init__(self, color: tuple, position: int, shape: String):
        self.color = color
        self.position = position
        self.shape = shape

size = 5
question_size = 18  ## 2 x (6 for one-hot vector of color), 3 for question type, 3 for question subtype
q_type_idx = 12
sub_q_type_idx = 15
"""Answer : [yes, no, rectangle, circle, r, g, b, o, k, y]"""

nb_questions = 10
dirs = './data'

try:
    os.makedirs(dirs)
except:
    print('directory {} already exists'.format(dirs))

def generate_position(objects):
    while True:
        pas = True
        position = np.random.randint(0, WIDTH**2)
        if len(objects) > 0:
            for object in objects:
                if object.position == position:
                    pas = False
        if pas:
            return position

def pos_to_coor(position):
    row = position // WIDTH
    col = position % WIDTH
    x_coor = (col / WIDTH) * IMG_SIZE + (IMG_SIZE / WIDTH) * 0.5
    y_coor = (row / WIDTH) * IMG_SIZE + (IMG_SIZE / WIDTH) * 0.5
    return x_coor, y_coor

def build_one_image():
    objects = []
    img = np.ones((IMG_SIZE, IMG_SIZE, 3)) * 255
    for color in colors:
        position = generate_position(objects)
        print(position)
        x_coor, y_coor = pos_to_coor(position)
        print(x_coor, y_coor)
        if random.random()<0.5:
            start = (int(x_coor - (IMG_SIZE / (2 * WIDTH)) + 5), int(y_coor - (IMG_SIZE / (2 * WIDTH)) + 5))
            print(start)
            end = (int(x_coor + (IMG_SIZE / (2 * WIDTH)) - 5), int(y_coor + (IMG_SIZE / (2 * WIDTH)) - 5))
            print(end)
            cv2.rectangle(img, start, end, color, -1)
            objects.append(Object(color, position, 'square'))
        else:
            center = (int(x_coor), int(y_coor))
            cv2.circle(img, center, size, color, -1)
            objects.append(Object(color, position, 'circle'))
    return img

img = build_one_image()
#cv2.imshow("Dataset", img)
#cv2.waitKey(5000)
cv2.imwrite('./test.png', img)
#cv2.destroyAllWindows("Dataset")
