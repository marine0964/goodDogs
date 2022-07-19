import json
import os
import cv2
import numpy as np
from os import walk
from tqdm import tqdm
from operator import itemgetter

TRAIN_LABEL= r"E:\k-ompanion_data\aihub\Training\label"
TRAIN_IMAGE= r"E:\k-ompanion_data\aihub\Training\image"
VALID_LABEL= r"E:\k-ompanion_data\aihub\Validation\label"
VALID_IMAGE= r"E:\k-ompanion_data\aihub\Validation\image"

# EMOTION_DICT = {"행복/즐거움":"happy",
#                 "편안/안정":"comfort",
#                 "불안/슬픔":"sad",
#                 "화남/불쾌":"unpleasant",
#                 "공포":"fear",
#                 "공격성":"aggressive"}

# EMTION_MAP = {"happy":0,
#               "comfort":1,
#               "sad":2,
#               "unpleasant":3,
#               "fear":4,
#               "aggressive":5}

# ACTION_MAP = {'BODYLOWER':0,
#               'BODYSCRATCH':1,
#               'BODYSHAKE':2,
#               'FEETUP':3,
#               'FOOTUP':4,
#               'HEADING':5,
#               'LYING':6,
#               'MOUNTING':7,
#               'SIT':8,
#               'TAILING':9,
#               'TAILLOW':10,
#               'TURN':11,
#               'WALKRUN':12}

ACTION_MAP = {'BODYLOWER':0,
              'FEETUP':1,
              'FOOTUP':2,
              'SIT':3}

def find_label_list(label_path):
    """
    json file - per one video
    """
    label_list = []
    action_list = []
    for (dirpath, dirnames, filenames) in walk(label_path):
        # print(dirpath)
        label_list.append((dirpath, dirnames, filenames))
        if filenames == []:
            action_list = dirnames
            # print(dirnames)
    label_list= [[i[0], i[2]] for i in label_list if i[1]==[]]

    clip_list = []
    for action, clips in label_list:
        clip_label = [action + "\\" + clip for clip in clips]
        clip_list.extend(clip_label)

    print("You have {} actions in {}".format(len(label_list), label_path))
    print("You have {} clips in {}".format(len(clip_list), label_path))

    return label_list, clip_list, action_list

def find_image_list(image_path):
    """
    jpg file - per one frame
    """
    image_list = []
    clip_list = []
    action_list = []
    for (dirpath, dirnames, filenames) in walk(image_path):
        if dirnames == []:
            clip_list.append(dirpath)
        elif filenames == [] and dirpath.split("\\")[-1]=='image':
            action_list.extend(dirnames)
    for clip in clip_list:
        for (dirpath, dirnames, filenames) in walk(clip):
            for image in filenames:
                image_list.append(dirpath+"\\"+image)

    print("You have {} actions in {}".format(len(action_list), image_path))
    print("You have {} clips in {}".format(len(clip_list), image_path))
    print("You have {} images in {}".format(len(image_list), image_path))

    return image_list, clip_list, action_list

if __name__=="__main__":
    
    label_list, label_clip_list, label_action_list = find_label_list(label_path=TRAIN_LABEL)
    print("-"*80)
    image_list, image_clip_list, image_action_list = find_image_list(image_path=TRAIN_IMAGE)
    
    assert label_action_list == image_action_list