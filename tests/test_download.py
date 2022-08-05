import os.path as osp

import pytest

from ntu_rgbd.download import login, download_url, extract, download_ntu


urls = [
    "https://rose1.ntu.edu.sg/dataset/actionRecognition/download/157",
    "https://rose1.ntu.edu.sg/dataset/actionRecognition/download/158",
]

file_names = [
    "nturgbd_skeletons_s001_to_s017.zip",
    "nturgbd_skeletons_s018_to_s032.zip",
]


@pytest.fixture
def session():
    return login()


def test_download(tmp_path, session):
    for i, url in enumerate(urls):
        file_name = download_url(session, url, tmp_path)
        assert file_name == file_names[i]

    for file_name in file_names:
        extract(osp.join(tmp_path, file_name), tmp_path)


def test_download_ntu(tmp_path):
    download_ntu(tmp_path)
