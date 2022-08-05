import os.path as osp
import pytest

from ntu_rgbd.data import load_path_list, load_video


@pytest.mark.parametrize("num_classes", [60, 120])
@pytest.mark.parametrize("benchmark", ["xsub", "xview"])
@pytest.mark.parametrize("split", ["train", "val"])
@pytest.mark.parametrize("skeleton_dims", [2, 3])
@pytest.mark.parametrize("max_frames", [10, 100])
def test_load_path_list(num_classes, benchmark, split, skeleton_dims, max_frames):
    tmp_path = "tmp"
    load_path_list(
        root=tmp_path, num_classes=num_classes, benchmark=benchmark, split=split
    )

    data = load_video(
        osp.join(tmp_path, "nturgb+d_skeletons", "S017C003P015R001A058.skeleton"),
        max_frames,
        4,
        skeleton_dims,
    )

    assert data.shape == (max_frames, 4, 25, skeleton_dims)
