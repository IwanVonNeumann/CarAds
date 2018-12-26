import os
import requests

from time import sleep

from scrap.parse import find_next_page_href, get_ad_hrefs, parse_sections_list, read_file

DOWNLOAD_DELAY = 0.5

PAGES_DIR = 'pages'
AD_LISTS_DIR = os.path.join(PAGES_DIR, 'ad_lists')
ADS_DIR = os.path.join(PAGES_DIR, 'ads')
SECTIONS_LIST_FILE_PATH = os.path.join(PAGES_DIR, 'sections_list.html')

URL_ROOT = "https://www.ss.com"
SECTIONS_LIST_URL = URL_ROOT + '/ru/transport/cars/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}


def store_everything():
    store_sections_list()
    store_ad_lists()
    store_ads()


def store_sections_list():
    print('storing sections list')
    create_if_does_not_exist(PAGES_DIR)
    store_page(url=SECTIONS_LIST_URL, path=SECTIONS_LIST_FILE_PATH)


def store_ad_lists():
    print('storing ads lists')
    create_if_does_not_exist(AD_LISTS_DIR)

    sections_list_file = read_file(SECTIONS_LIST_FILE_PATH)
    sections_list = parse_sections_list(sections_list_file)

    for section in sections_list:
        store_ad_lists_from_section(section)


def create_if_does_not_exist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def store_page(url, path):
    print('storing {} -> {}'.format(url, path))

    response = requests.get(url, headers=headers)
    with open(path, 'wb') as output_file:
        output_file.write(response.text.encode('utf8'))


def store_ad_lists_from_section(section):
    page_number = 1
    next_page_href = section["href"]

    while next_page_href is not None:
        page_url = URL_ROOT + next_page_href
        ads_list_file_path = generate_ads_list_file_path(section["name"], page_number)
        store_page(page_url, ads_list_file_path)

        ads_list_page_file = read_file(ads_list_file_path)
        next_page_href = find_next_page_href(ads_list_page_file)

        page_number += 1
        sleep(DOWNLOAD_DELAY)

    print("all ad lists stored for {}".format(section["name"]))


# TODO find usages
def concat_url(href):
    return URL_ROOT + href


def generate_ads_list_file_path(section_name, page_number):
    file_name = '{}_{}.html'.format(format_section_name(section_name), page_number)
    return os.path.join(AD_LISTS_DIR, file_name)


def format_section_name(section_name):
    return section_name.replace(" ", "_").lower()


def store_ads():
    print('storing ads')
    create_if_does_not_exist(ADS_DIR)

    for ads_list_file in os.listdir(AD_LISTS_DIR):
        filename = os.fsdecode(ads_list_file)
        ads_list_page_file_path = os.path.join(AD_LISTS_DIR, filename)
        ads_list_page_file = read_file(ads_list_page_file_path)
        store_ads_from_page(ads_list_page_file)
        print("all ads from {} stored".format(filename))


def store_ads_from_page(ads_list_page_file):
    hrefs = get_ad_hrefs(ads_list_page_file)
    for href in hrefs:
        url = concat_url(href)
        file_name = generate_ad_file_name(href)
        path = os.path.join(ADS_DIR, file_name)
        store_page(url, path)
        sleep(DOWNLOAD_DELAY)


def generate_ad_file_name(href):
    COMMON_PART = r"/msg/ru/transport/cars/"
    tail = href.partition(COMMON_PART)[2]
    return tail.replace("/", "_")
