# NTU RGB+D Dataset Helper Library

- Download dataset in parallel using curl (requires a cookie)

## Quick tour

download skeleton datasets

run `./scripts/extract.sh <path>` to extract files to path

```
>>> from ntu_rgbd import SkeletonDataset

>>> dataset = SkeletonDataset(root="skeletons")
```

## Installation

`pip install -e .`

###
