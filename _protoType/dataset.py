import json
import os
import csv
from os import walk
from tqdm import tqdm
from utils import *

def get_json(clip, action=None):
    json_path = TRAIN_LABEL+"\\"+action+"\\"+clip+".json"
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
            # print("MATCHED")
            # print(frame_num)
            # print(timestamp_num)
            # print(bbox)
            return frame_num, timestamp_num, bbox
        else:
        #     print("NO MATCHED")
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
        annotations = json_object["annotations"] # 94
        emotion = metadata["inspect"]["emotion"]
        emotion = EMOTION_DICT[emotion]
        # action = metadata["inspect"]["action"]
        emotion_id = EMTION_MAP[emotion]
        action_id = ACTION_MAP[action]
        
        frame_num, timestamp_num, bbox = synchronize(annotations, frame_num, timestamp_num)
            
        anno_dict["filename"] = TRAIN_IMAGE+"\\"+action+"\\"+ working_clip+"\\" + "frame_{}_timestamp_{}.jpg".format(frame_num, timestamp_num)
        anno_dict["width"] = bbox["width"]
        anno_dict["height"] = bbox["height"]
        anno_dict["class"] = action
        anno_dict["xmin"] = bbox["x"]
        anno_dict["ymin"] = bbox["y"]
        anno_dict["xmax"] = bbox["x"] + bbox["width"]
        anno_dict["ymax"] = bbox["y"] + bbox["height"]
        anno_dict["labels"] = action_id
        # anno_dict["emotion"] = emotion
        
        # anno_dict["emotion"] = emotion_id
        # print(anno_dict)
        total_list.append(anno_dict)
    return total_list
    
def get_frame_time_num(image_list):
    """
    get frame_num, timestamp_num from image_list
    """
    print(">> Get frame_num, timestamp_num from image_list")
    frame_time_list = []
    for img_path in tqdm(image_list):
        # i : full path
        clip = img_path.split("\\")[-2] # "20201022_dog-bodylower-000028.mp4"
        frame_num = img_path.split("\\")[-1].split("_")[1] # frame_0_timestamp_0.jpg
        timestamp_num = img_path.split("\\")[-1].split("_")[3][:-4]
        frame_time_list.append((clip, frame_num, timestamp_num))
    return frame_time_list
    
def write_csv(total_list, path):
    # fieldnames = ["path", "x1", "y1", "x2", "y2", "action", "emotion"]
    fieldnames = ["filename", "width", "height","class", "xmin", "ymin", "xmax", "ymax", "labels"]
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(total_list)


if __name__=="__main__":
    image_list, image_clip_list, image_action_list = find_image_list(image_path=TRAIN_IMAGE)
    # print(image_list[1]) # ~\Training\image\BODYLOWER\20201022_dog-bodylower-000028.mp4\frame_0_timestamp_0.jpg
    # print(image_clip_list[0]) # \Training\image\BODYLOWER\20201022_dog-bodylower-000028.mp4
    frame_time_list = get_frame_time_num(image_list)
    total_list = get_clip_annotation(frame_time_list)
    print(len(total_list))
    path = r"E:\k-ompanion_data\aihub\Training\train3.csv"
    write_csv(total_list, path)