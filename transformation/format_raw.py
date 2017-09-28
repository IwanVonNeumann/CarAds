from db.mongo_client import c


def format_raw_records():
    items = c("ads_raw").find_all()
    for x in items:
        format_raw_record(x)
        c("ads_raw").update(x)


def format_raw_record(record):
    record["price"] = format_raw_price(record["price"])
    record["color"] = format_raw_color(record["color"])
    return record


def format_raw_color(color):
    if color is not None:
        color = color.replace("\xa0", "")
        color = color.replace("  ", " ")
        color = color.rstrip()
    return color


def format_raw_price(price):
    if price is not None:
        price = price.split('€', 1)[0]
        price = price.replace(" ", "")
    return price
