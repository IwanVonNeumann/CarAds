def remove_incomplete(items, log=False):
    items = remove_by_empty_secondary_features(items, log=log)
    items = remove_by_primary_attribute_none(items, log=log)
    items = remove_by_value(items, "body_type", "-", log=log)
    return items


def remove_by_primary_attribute_none(items, log=False):
    primary_attributes = [
        "mileage", "color", "city", "price", "engine", "model", "release_year", "transmission", "body_type"
    ]

    for attribute in primary_attributes:
        items = remove_by_none_value(items, attribute, log=log)
    return items


def remove_by_none_value(items, field, log=False):
    return remove_by_value(items, field, None, log=log)


def remove_by_value(items, field, value, log=False):
    filtered = [x for x in items if x[field] != value]
    if log:
        records_removed = len(items) - len(filtered)
        print("Removing by {}={}: {}".format(field, value, records_removed))
    return filtered


def remove_by_empty_secondary_features(items, log=False):
    filtered = [x for x in items if len(x["secondary_features"]) > 0]
    if log:
        records_removed = len(items) - len(filtered)
        print("Removing by empty secondary_features: {}".format(records_removed))
    return filtered
