from typing import Callable

import torch
from torch.utils.data import Dataset

from ntu_rgbd.utils import (
    load_path_list,
    load_2d_skeleton,
    load_3d_skeleton,
    load_label,
)


class SkeletonDataset(Dataset):
    def __init__(
        self,
        root: str,
        num_classes: int = 60,
        benchmark: str = "xsub",
        split: str = "train",
        skeleton_dims: int = 3,
        max_frames: int = 300,
        max_skeletons: int = 4,
        transform: Callable = None,
    ):
        self.max_frames = max_frames
        self.max_skeletons = max_skeletons

        assert skeleton_dims in [2, 3]

        if skeleton_dims == 3:
            self.load_skeleton = load_3d_skeleton
        if skeleton_dims == 2:
            self.load_skeleton = load_2d_skeleton

        self.transform = transform

        self.path_list = load_path_list(root, num_classes, benchmark, split)

    def __getitem__(self, idx):
        path = self.path_list[idx]

        x = self.load_skeleton(path, self.max_frames, self.max_skeletons)
        x = torch.Tensor(x)

        if self.transform is not None:
            x = self.transform(x)

        y = load_label(path)

        return x, y

    def __len__(self):
        return len(self.path_list)
