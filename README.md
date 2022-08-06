# NTU RGB+D Dataset Helper Library

- Download dataset in parallel using curl (requires a cookie)

## Quick tour

`pip install -e .` to install library

```
>>> from ntu_rgbd import NTURGBD

>>> dataset = NTURGBD(root="skeletons")
```

```
class NTURGBD:
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
        download: bool = True,
    ):
```
