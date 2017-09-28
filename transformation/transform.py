from transformation.remove_incomplete import remove_by_value
from utils.utils import replace_rare_values


def transform_fields(items, log=False):
    items = remove_free_text(items)  # not analyzed now
    items = split_engine_into_type_and_volume(items)
    items = remove_by_engine_volume_zero(items, log=log)
    items = extract_metallic_paint_type(items)
    items = binarize_checkup(items)
    items = make_mileages_int(items)
    items = remove_by_mileage_over_million(items)
    items = make_prices_float(items)
    items = remove_by_price_below_50(items)
    items = remove_release_month(items)
    items = extract_age_from_release_year(items)
    items = remove_by_age_over_100(items)
    items = merge_city_lithuania(items)
    items = merge_transmissions(items)
    items = merge_rare_cities(items, log=log)
    return items


def make_int(items, field):
    for x in items:
        x[field] = int(x[field])
    return items


def split_engine_into_type_and_volume(items):
    for x in items:
        engine = x["engine"]
        parts = engine.split(" ")
        engine_volume = parts[0]
        engine_type = parts[1]
        x["engine_volume"] = engine_volume
        x["engine_type"] = engine_type
        x.pop("engine")
    return items


# Removing by engine_volume=0.0: 2
def remove_by_engine_volume_zero(items, log=False):
    return remove_by_value(items, "engine_volume", "0.0", log=log)


def extract_metallic_paint_type(items):
    for x in items:
        color = x["color"]
        if color.endswith("металлик"):
            color = color.split(" ")[0]
            x["color"] = color
            x["paint_metallic"] = True
        else:
            x["paint_metallic"] = False
    return items


def binarize_checkup(items):
    for x in items:
        x["checkup"] = binarize_checkup_one(x["checkup"])
    return items


def binarize_checkup_one(checkup):
    if checkup in [None, "Без техосмотра", "0.0"]:
        return False

    checkup = extract_year_month_from_checkup(checkup)

    if checkup["year"] < 2017:
        return False
    if checkup["year"] > 2017:
        return True
    if checkup["month"] > 8:
        return True
    return False


def extract_year_month_from_checkup(checkup):
    checkup = checkup.replace(" ", "")
    parts = checkup.split(".")
    if parts[0].startswith("201"):
        year = parts[0]
        month = parts[1]
    else:
        year = parts[1]
        month = parts[0]
    if month.startswith("0"):
        month = month.replace("0", "")
    return {"year": int(year), "month": int(month)}


def remove_free_text(items):
    for x in items:
        x.pop("free_text")
    return items


def make_mileages_int(items):
    for x in items:
        x["mileage"] = make_mileage_int(x["mileage"])
    return items


def make_mileage_int(mileage):
    return int(mileage.replace(" ", "").split(".")[0])


def remove_by_mileage_over_million(items):
    return [x for x in items if x["mileage"] < 1E6]


def make_prices_float(items):
    for x in items:
        x["price"] = float(x["price"])
    return items


def remove_by_price_below_50(items):
    return [x for x in items if x["price"] > 50]


def remove_release_month(items):
    for x in items:
        year = extract_year_from_release_date(x["release_year"])
        x["release_year"] = year
    return items


def extract_year_from_release_date(release_date):
    return int(release_date.split(" ")[0])


def extract_age_from_release_year(items):
    for x in items:
        x["age"] = 2017 - x["release_year"]
        x.pop("release_year")
    return items


def remove_by_age_over_100(items):
    return [x for x in items if x["age"] <= 100]


def merge_city_lithuania(items):
    for x in items:
        if x["city"].startswith("Литва"):
            x["city"] = "Литва"
    return items


def merge_transmissions(items):
    for x in items:
        x["transmission"] = merge_transmission(x["transmission"])
    return items


def merge_transmission(transmission):
    if transmission.startswith("Ручная"):
        return "Ручная"
    if transmission.startswith("Автомат"):
        return "Автомат"


def merge_rare_cities(items, log=False):
    return replace_rare_values(items, "city", 0.05, log=log)
