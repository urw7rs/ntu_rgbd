import itertools

from torch.utils.data import DataLoader

from ntu_rgbd import SkeletonDataset


def test_dataset():
    for num_classes, benchmark, split, skeleton_dims, max_frames in itertools.product(
        [60, 120], ["xsub", "xview"], ["train", "val"], [2, 3], [10, 100]
    ):
        dataset = SkeletonDataset(
            root="skeletons",
            num_classes=num_classes,
            benchmark=benchmark,
            split=split,
            skeleton_dims=skeleton_dims,
            max_frames=max_frames,
            max_skeletons=4,
        )
        x, y = dataset[0]

        assert (
            x.shape[0] == skeleton_dims and x.shape[1] == max_frames and x.shape[3] == 4
        )

        data_loader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=2)
        x, y = next(iter(data_loader))

        assert (
            x.shape[0] == 2
            and x.shape[1] == skeleton_dims
            and x.shape[2] == max_frames
            and x.shape[4] == 4
        )
