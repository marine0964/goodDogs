import json
import os
import csv
from os import walk
from tqdm import tqdm
from kompanion_utils import *
import shutil
from glob import glob
from sklearn.model_selection import train_test_split

def get_json(clip, action=None):
    json_path = VALID_LABEL+"\\"+action+"\\"+clip+".json"
    with open(json_path, "r", encoding="utf8") as f:
        json_object = json.load(f)
    return json_object

def synchronize(annotations, frame_num, timestamp_num):
    for i in range(len(annotations)):
        frame_number = annotations[i]["frame_number"]
        timestamp = annotations[i]["timestamp"]
        frame_num = int(frame_num)
        timestamp_num = int(timestamp_num)
        if frame_num == frame_number and timestamp_num == timestamp :
            bbox = annotations[i]["bounding_box"]
            return frame_num, timestamp_num, bbox
        else:
            pass

def get_clip_annotation(frame_time_list):
    """
    get annotation dictionary
    """
    print(">> Get annotation dictionary")
    total_list = []
    for i in tqdm(range(len(frame_time_list))): # get video name
        anno_dict = dict()
        working_clip = frame_time_list[i][0]
        # before = i-1 if i != 0 else 0
        before_clip = frame_time_list[i-1 if i != 0 else 0][0]
        frame_num = frame_time_list[i][1]
        timestamp_num = frame_time_list[i][2]
        
        action = working_clip.split("-")[1].upper()
        if before_clip != working_clip:
            json_object = get_json(working_clip, action)
        elif i==0:
            json_object = get_json(working_clip, action)
        else:
            pass

        metadata = json_object["metadata"]
        annotations = json_object["annotations"] 
        # emotion = metadata["inspect"]["emotion"]
        # emotion = EMOTION_DICT[emotion]
        # emotion_id = EMTION_MAP[emotion]
        action_id = ACTION_MAP[action]
        
        frame_num, timestamp_num, bbox = synchronize(annotations, frame_num, timestamp_num)
            
        anno_dict["filename"] = VALID_IMAGE+"\\"+action+"\\"+ working_clip+"\\" + "frame_{}_timestamp_{}.jpg".format(frame_num, timestamp_num)
        anno_dict["width"] = bbox["width"]
        anno_dict["height"] = bbox["height"]
        anno_dict["class"] = action
        anno_dict["xcen"] = bbox["x"]+ (bbox["width"]/2)
        anno_dict["ycen"] = bbox["y"]+ (bbox["height"]/2)
        anno_dict["labels"] = action_id
        total_list.append(anno_dict)
    return total_list
    
def get_frame_time_num(image_list):
    """
    get frame_num, timestamp_num from image_list
    """
    print(">> Get frame_num, timestamp_num from image_list")
    frame_time_list = []
    for img_path in tqdm(image_list):
        clip = img_path.split("\\")[-2] # "20201022_dog-bodylower-000028.mp4"
        frame_num = img_path.split("\\")[-1].split("_")[1] # frame_0_timestamp_0.jpg
        timestamp_num = img_path.split("\\")[-1].split("_")[3][:-4]
        frame_time_list.append((clip, frame_num, timestamp_num))
    return frame_time_list

def make_files(total_list):
    """
    make txt label files
    """
    for dict_data in tqdm(total_list):
        original = dict_data["filename"] # full name
        clip = original.split("\\")[-2] # "20201022_dog-bodylower-000028.mp4"
        file_name = original.split("\\")[-1]
        new_name = clip +"-"+ file_name
        target = VALID_IMAGE+ "\\" + new_name
        # print(target)
        # os.rename(original, target)
        shutil.copyfile(original, target)
        class_id = dict_data["labels"]
        xcen = dict_data["xcen"]
        ycen = dict_data["ycen"]
        w = dict_data["width"]
        h = dict_data["height"]
        txt_path = VALID_LABEL+ "\\" + new_name[:-3] + "txt"
        # print(txt_path)
        with open("{}".format(txt_path), 'w') as f:
            f.write('%s,%s,%s,%s,%s' % (class_id, xcen, ycen, w, h))

def check_names(img_path, lab_path):
    # path1 = r"E:\k-ompanion_data\aihub\Validation\label"
    # path2 = r"E:\k-ompanion_data\aihub\Validation\image" 
    file_list1 = os.listdir(lab_path) # label
    file_list1 = [ k[:-4] for k in file_list1]
    file_list2 = os.listdir(img_path)
    for i in tqdm(file_list2):
        if i[:-4] not in file_list1:
            # more images
            print("there is no label corresponding to")
            print(i)
    file_list1 = os.listdir(img_path) # label
    file_list1 = [ k[:-4] for k in file_list1]
    file_list2 = os.listdir(lab_path)
    for j in tqdm(file_list2):
        if j[:-4] not in file_list1:
            # more labels
            print("there is no image corresponding to")
            print(j)

def count_files(path):
    file_list = os.listdir(path)
    print(len(file_list))

def txt_list(path):
    """
    yolo txt file -> yaml
    """
    print(path+"\\"+'*.jpg')
    img_list = glob(path+"\\"+'*.jpg')
    print(len(img_list))

    train_img_list, val_img_list = train_test_split(img_list, test_size=0.2, random_state=2000)

    print(len(train_img_list), len(val_img_list))
    with open(".\\"+'train.txt', 'w') as f:
        f.write('\n'.join(train_img_list) + '\n')

    with open(".\\"+'val.txt', 'w') as f:
        f.write('\n'.join(val_img_list) + '\n')


if __name__=="__main__":
    # count_files(r"E:\k-ompanion_data\aihub\Training\label")
    # count_files(r"E:\k-ompanion_data\aihub\Training\image")

    # image_list, image_clip_list, image_action_list = find_image_list(image_path=TRAIN_IMAGE)
    # frame_time_list = get_frame_time_num(image_list)
    # total_list = get_clip_annotation(frame_time_list)
    # make_files(total_list)

    # valid
    # image_list, image_clip_list, image_action_list = find_image_list(image_path=VALID_IMAGE)
    # frame_time_list = get_frame_time_num(image_list)
    # total_list = get_clip_annotation(frame_time_list)
    # make_files(total_list)

    # count_files(r"E:\k-ompanion_data\aihub\Validation\label")
    # count_files(r"E:\k-ompanion_data\aihub\Validation\image")
    # check()
    # after naming
    path = r"E:\k-ompanion_data\aihub\images"
    txt_list(path)
