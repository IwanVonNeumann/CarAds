import os

from os.path import isfile, join

from db.mongo_client import c
from scrap.parse import read_file, parse_ad

ADS_PATH = r"D:\Data\pages\ads"


def list_files(path):
    return [f for f in os.listdir(path) if isfile(join(path, f))]


def init_db():
    files = list_files(ADS_PATH)
    i = 1

    for file_name in files:
        path = os.path.join(ADS_PATH, file_name).replace("\\", "/")
        content = read_file(path)
        ad = parse_ad(content)
        c("ads_raw").insert_one(ad.__dict__)
        print(i, "/", len(files), ":", file_name)
        i += 1
