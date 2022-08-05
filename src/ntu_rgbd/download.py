import os.path as osp

import cgi
import getpass

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import zipfile

login_url = "https://rose1.ntu.edu.sg/login/"
skeleton_urls = [
    "https://rose1.ntu.edu.sg/dataset/actionRecognition/download/157",
    "https://rose1.ntu.edu.sg/dataset/actionRecognition/download/158",
]
skeleton_file_names = [
    "nturgbd_skeletons_s001_to_s017.zip",
    "nturgbd_skeletons_s018_to_s032.zip",
]


def login():
    s = requests.Session()
    r = s.get(login_url)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, features="html.parser")
    csrftoken = soup.find("input", dict(name="csrfmiddlewaretoken"))["value"]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        ),
        "Referer": "https://rose1.ntu.edu.sg/login/",
    }

    print(
        "Type your username and password for http://rose1.ntu.edu.sg to download dataset"
    )
    username = input("Username: ")
    password = getpass.getpass()

    r = s.post(
        "https://rose1.ntu.edu.sg/login/",
        data={
            "csrfmiddlewaretoken": csrftoken,
            "username": username,
            "password": password,
        },
        headers=headers,
    )
    r.raise_for_status()

    return s


def download_url(s, url, dst):
    with s.get(url, stream=True) as r:
        r.raise_for_status()

        headers = r.headers
        total = int(headers.get("content-length", 0))

        string = headers.get("Content-Disposition", None)

        from_url = url.split("/")[-1]
        if string is None:
            file_name = from_url
        else:
            value, params = cgi.parse_header(string)
            file_name = params.get("filename", from_url)

        path = osp.join(dst, file_name)

        if osp.exists(path):
            print(f"{file_name} already downloaded")
            return file_name

        with tqdm.wrapattr(
            open(path, "wb"),
            "write",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            total=total,
        ) as fout:
            for chunk in r.iter_content(chunk_size=1024):
                fout.write(chunk)

        return file_name


def extract(src, dst):
    with zipfile.ZipFile(src, "r") as zip_ref:
        zip_ref.extractall(dst)


def download_ntu(root, num_classes):
    file_names = skeleton_file_names
    urls = skeleton_urls

    if num_classes == 60:
        urls = file_names[0:1]
        file_names = file_names[0:1]

    session = None
    for url, file_name in zip(urls, file_names):
        if not osp.exists(osp.join(root, file_name)):
            if session is None:
                session = login()

            download_url(session, url, root)

    for i, file_name in enumerate(file_names):
        path = osp.join(root, file_name)
        if i == 0:
            extract(path, root)
        if i == 1:
            extract(path, osp.join(root, "nturgb+d_skeletons"))
