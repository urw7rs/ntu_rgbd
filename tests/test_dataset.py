import pytest

from torch.utils.data import DataLoader

from ntu_rgbd import NTURGBD


@pytest.mark.parametrize("num_classes", [60, 120])
@pytest.mark.parametrize("benchmark", ["xsub", "xview"])
@pytest.mark.parametrize("split", ["train", "val"])
@pytest.mark.parametrize("skeleton_dims", [2, 3])
@pytest.mark.parametrize("max_frames", [10, 100])
def test_dataset(num_classes, benchmark, split, skeleton_dims, max_frames):
    dataset = NTURGBD(
        root="tmp",
        num_classes=num_classes,
        benchmark=benchmark,
        split=split,
        skeleton_dims=skeleton_dims,
        max_frames=max_frames,
        max_skeletons=4,
        download=False,
    )
    x, y = dataset[0]

    assert x.shape == (max_frames, 4, 25, skeleton_dims)

    data_loader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=2)
    x, y = next(iter(data_loader))

    assert x.shape == (2, max_frames, 4, 25, skeleton_dims)
