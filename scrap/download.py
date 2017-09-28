import os
from time import sleep

import requests

from scrap.parse import get_next_page_href, get_ad_hrefs

URL_ROOT = "https://www.ss.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}


def store_page(url, path):
    print(url, "->", path)
    response = requests.get(url, headers=headers)
    with open(path, 'wb') as output_file:
        output_file.write(response.text.encode('utf8'))


def store_section(section, dir):
    i = 1
    page_url = get_url(section["href"])

    while True:
        path = generate_section_file_path(dir, section["name"], i)
        store_page(page_url, path)
        print(i, path, page_url)

        next_href = get_next_page_href(path)
        if next_href is None:
            break

        page_url = get_url(next_href)
        i += 1
        sleep(1)

    print("That's all for", section["name"])


def get_url(href):
    return URL_ROOT + href


def generate_section_file_path(dir, section_name, i):
    return os.path.join(dir, get_section_file_name_base(section_name) + str(i) + ".html").replace("\\", "/")


def get_section_file_name_base(section_name):
    return section_name.replace(" ", "_").lower() + "_"


def store_ads(ads_dir):
    sections_dir = r"pages\sections"
    for section_file in os.listdir(sections_dir):
        filename = os.fsdecode(section_file)
        section_page_path = os.path.join(sections_dir, filename).replace("\\", "/")
        store_ads_from_page(ads_dir, section_page_path)
        print("Done for", filename)


def store_ads_from_page(dir, section_page_path):
    hrefs = get_ad_hrefs(section_page_path)
    for href in hrefs:
        url = get_url(href)
        file_name = generate_ad_file_name(href)
        path = os.path.join(dir, file_name)
        store_page(url, path)
        sleep(1)
    print("Done for", section_page_path)


def generate_ad_file_name(href):
    COMMON_PART = r"/msg/ru/transport/cars/"
    tail = href.partition(COMMON_PART)[2]
    return tail.replace("/", "_")
