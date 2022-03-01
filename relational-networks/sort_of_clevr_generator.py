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
parser.add_argument('--seed', type=int, default=3, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--t-subtype', type=int, default=-1,
                    help='Force ternary questions to be of a given type')
args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)

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
question_size = len(colors) + 2 + 3 ## (number of colors for one-hot vector of color), 3 for question type (nonbinary VS binary), 3 for question subtype
q_type_idx = len(colors)
sub_q_type_idx = len(colors) + 2
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
            cv2.circle(img, center, int((IMG_SIZE / (2 * WIDTH)) - 5), color, -1)
            objects.append(Object(color, position, 'circle'))
    return img, objects

def build_nonrelational_questions(objects):
    nonrelational_questions = []
    nonrelational_answers = []
    for _ in range(nb_questions):
        question = np.zeros((question_size))
        color = random.randint(0, len(colors) - 1)
        question[color] = 1
        question[q_type_idx] = 1
        subtype = random.randint(0,2)
        question[subtype+sub_q_type_idx] = 1
        nonrelational_questions.append(question)
        """Answer : [yes, no, rectangle, circle, r, g, b, o, k, y]"""
        if subtype == 0:
            """query shape->rectangle/circle"""
            if objects[color].shape == 'square':
                answer = 2
            else:
                answer = 3

        elif subtype == 1:
            """query horizontal position->yes/no"""
            print(objects[color].position)
            if pos_to_coor(objects[color].position)[0] < IMG_SIZE / 2:
                answer = 0
            else:
                answer = 1

        elif subtype == 2:
            """query vertical position->yes/no"""
            if pos_to_coor(objects[color].position)[1] > IMG_SIZE / 2: # Be aware, the y axis runs downward!!!
                answer = 0
            else:
                answer = 1
        nonrelational_answers.append(answer)
    return nonrelational_questions, nonrelational_answers

def build_binary_questions(objects):
    binary_questions = []
    binary_answers = []
    for _ in range(nb_questions):
        question = np.zeros((question_size))
        color = random.randint(0, len(colors) - 1)
        question[color] = 1
        question[q_type_idx+1] = 1
        subtype = random.randint(0,2)
        question[subtype+sub_q_type_idx] = 1
        binary_questions.append(question)

        if subtype == 0:
            """closest-to->rectangle/circle"""
            my_obj = objects[color]
            dist_list = [((np.subtract(pos_to_coor(my_obj.position), pos_to_coor(obj.position))) ** 2).sum() for obj in objects]
            dist_list[dist_list.index(0)] = float('inf') # The distance to the element itself should not be considered
            closest = dist_list.index(min(dist_list))
            if objects[closest].shape == 'square':
                answer = 2
            else:
                answer = 3
                
        elif subtype == 1:
            """furthest-from->rectangle/circle"""
            my_obj = objects[color]
            dist_list = [((np.subtract(pos_to_coor(my_obj.position), pos_to_coor(obj.position))) ** 2).sum() for obj in objects]
            furthest = dist_list.index(max(dist_list))
            if objects[furthest].shape == 'square':
                answer = 2
            else:
                answer = 3

        elif subtype == 2:
            """count->1~6"""
            my_obj = objects[color]
            count = -1
            for obj in objects:
                if obj.shape == my_obj.shape:
                    count +=1
            answer = count+4 # Not 'yes', 'no', 'square' or 'circle' (make this clear with the +4)

        binary_answers.append(answer)
    return binary_questions, binary_answers

def build_dataset_item():
    img, objects = build_one_image()
    nonrelational_questions, nonrelational_answers = build_nonrelational_questions(objects)
    binary_questions, binary_answers = build_binary_questions(objects)

    binary_relations = (binary_questions, binary_answers)
    norelations = (nonrelational_questions, nonrelational_answers)
    
    #img = img/255.
    dataset = (img, norelations, binary_relations)
    return dataset

img, norelations, binary_relations = build_dataset_item()
cv2.imwrite('./test.png', img)