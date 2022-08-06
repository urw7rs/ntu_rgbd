import os
import numpy as np

from typing import List
from ntu_rgbd.missing_files import missing_files
from ntu_rgbd.label_map import label_map

train_subjects = [
    int(c)
    for c in (
        "1,2,4,5,8,9,"
        "13,14,15,16,17,18,19,"
        "25,27,28,"
        "31,34,35,38,"
        "45,46,47,49,"
        "50,52,53,54,55,56,57,58,59,"
        "70,74,78,"
        "80,81,82,83,84,85,86,89,"
        "91,92,93,94,95,97,98,"
        "100,103"
    ).split(",")
]

train_cameras = [2, 3]


def load_path_list(
    root: str, num_classes: int, benchmark: str, split: str
) -> List[str]:
    """extracts all skeletons to the root folder in the expected format."""

    assert split != "test"

    file_list_path = os.path.join(root, f"{num_classes}_{benchmark}_{split}.txt")

    if not os.path.exists(file_list_path):
        # create file list
        file_list = []
        for filename in os.listdir(root):
            # skip non skeleton files first
            if filename.split(".")[-1] != "skeleton":
                continue
            if num_classes == 60 and int(filename[1:4]) > 17:
                continue
            if filename.split(".")[0] in missing_files:
                continue

            if benchmark == "xsub":
                eval_id = int(filename[9:12])
                train_group = train_subjects
            elif benchmark == "xview":
                eval_id = int(filename[5:8])
                train_group = train_cameras

            if eval_id in train_group:
                curr_split = "train"
            else:
                curr_split = "val"

            if curr_split == split:
                file_list.append(filename)

        with open(file_list_path, "w") as f:
            file_list = f.writelines("\n".join(file_list) + "\n")

    with open(file_list_path, "r") as f:
        file_list = f.read().splitlines()

    path_list = []
    for filename in file_list:
        path = os.path.join(root, filename)
        path_list.append(path)

    return path_list


def load_sequence(
    path: str,
    max_frames: int,
    max_skeletons: int,
    skeleton_dim: int,
    use_depth: bool = False,
) -> List:
    with open(path, "r") as f:
        num_frames = int(f.readline())

        frames = []
        for i in range(num_frames):
            num_skeletons = int(f.readline())

            skeletons = []
            for j in range(num_skeletons):
                # skip metadata
                f.readline()

                num_joints = int(f.readline())
                skeleton = []
                for _ in range(num_joints):
                    # [3]
                    line = f.readline()

                    joint = line.split()

                    if skeleton_dim == 3:
                        joint = joint[:3]
                    if skeleton_dim == 2:
                        if use_depth:
                            joint = joint[3:5]
                        else:
                            joint = joint[5:7]

                    # convert strings to floats
                    joint = list(map(float, joint))

                    # [num_joints, 3]
                    skeleton.append(joint)
                # [num_skeletons, num_joints, 3]
                skeletons.append(skeleton)
            # [num_frames, num_skeletons, num_joints, coords]
            frames.append(skeletons)

    # [num_frames, num_skeletons, num_joints, coords]
    return pad_to_np(frames, max_frames, max_skeletons)


def pad_to_np(data: List, max_frames: int, max_skeletons: int):
    max_joints = 0
    max_coords = 0

    for skeletons in data:
        for joints in skeletons:
            max_joints = max(len(joints), max_joints)

            for joint in joints:
                max_coords = max(len(joint), max_coords)

    np_data = np.zeros(
        (max_frames, max_skeletons, max_joints, max_coords), dtype=np.float32
    )

    if max_frames < len(data):
        data = data[:max_frames]

    for t, skeletons in enumerate(data):
        for m, skeleton in enumerate(skeletons):
            np_data[t, m] = np.array(skeleton)

    return np_data


def load_label(path: str) -> int:
    filename = os.path.basename(path)
    return int(filename[17:20]) - 1


def to_class(label: int) -> str:
    return label_map[label]
