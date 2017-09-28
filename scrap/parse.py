from bs4 import BeautifulSoup

from model.rawad import RawAd


def read_file(filename):
    with open(filename, encoding="utf8") as input_file:
        text = input_file.read()
    return text


def get_sections_list():
    IGNORED_SECTIONS = {"Другие марки"}

    results = []

    html_text = read_file("pages/list.html")
    soup = BeautifulSoup(html_text, "html.parser")

    model_links = soup.find("td", {"width": "75%", "valign": "top"}).find_all('a', {'class': 'a_category'})
    for link in model_links:
        if link.text not in IGNORED_SECTIONS:
            results.append({
                "name": link.text,
                "href": link.get('href')
            })

    return results


def get_next_page_href(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    nav_links = soup.find_all("a", {"name": "nav_id"})

    if len(nav_links) == 0:
        return None

    next_link = nav_links.pop()
    href = next_link.get("href")

    if leads_to_first_page(href):
        return None

    return href


def leads_to_first_page(href):
    return not href.endswith(".html")


def get_ad_hrefs(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    results = []
    ad_links = soup.find_all("a", {"class": "am"})
    for link in ad_links:
        results.append(link.get("href"))

    return results


ad_properties = {

    "tdo_31": "model",
    "tdo_18": "release_year",
    "tdo_15": "engine",
    "tdo_35": "transmission",
    "tdo_16": "mileage",
    "tdo_17": "color",
    "tdo_32": "body_type",
    "tdo_223": "checkup"
}


def parse_ad(html_text):
    ad = RawAd()

    soup = BeautifulSoup(html_text, "html.parser")

    price_element = soup.find(attrs={"class": "ads_price"})

    if price_element is not None:
        ad.price = price_element.text

    primary_params = soup.find_all("td", {"class": "ads_opt"})

    for x in primary_params:
        element_id = x["id"]
        prop = ad_properties.get(element_id)
        if prop is not None:
            setattr(ad, prop, x.text)

    contacts = soup.find_all("td", {"class": "ads_contacts_name"})
    for x in contacts:
        if x.text == "Место:":
            ad.city = x.nextSibling.text

    free_text = soup.find("div", {"id": "msg_div_msg"})
    ad.free_text = free_text.text

    secondary_params = soup.find_all("b", {"class": "auto_c"})

    for x in secondary_params:
        ad.secondary_features.append(x.text)

    return ad
