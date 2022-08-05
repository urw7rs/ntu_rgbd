import os.path as osp

from ntu_rgbd.download import download_ntu
from ntu_rgbd.data import (
    load_path_list,
    load_video,
    load_label,
)


class NTURGBD:
    def __init__(
        self,
        root: str,
        num_classes: int = 60,
        benchmark: str = "xsub",
        split: str = "train",
        skeleton_dims: int = 3,
        use_depth: bool = False,
        max_frames: int = 300,
        max_skeletons: int = 4,
        download=False,
    ):
        self.max_frames = max_frames
        self.max_skeletons = max_skeletons

        assert skeleton_dims in [2, 3]
        if use_depth:
            assert skeleton_dims == 2

        self.skeleton_dims = skeleton_dims
        self.use_depth = use_depth

        if download:
            download_ntu(root, num_classes)

        self.path_list = load_path_list(
            osp.join(root, "nturgb+d_skeletons"), num_classes, benchmark, split
        )

    def __getitem__(self, idx):
        path = self.path_list[idx]

        x = load_video(
            path,
            self.max_frames,
            self.max_skeletons,
            self.skeleton_dims,
            self.use_depth,
        )
        y = load_label(path)

        return x, y

    def __len__(self):
        return len(self.path_list)
