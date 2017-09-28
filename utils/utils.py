from collections import Counter


def extract_feature(items, feature):
    return [x[feature] for x in items]


def feature_unique_values(items, feature):
    return {x[feature] for x in items}


def calculate_absolute_frequencies(values):
    return dict(Counter(values))


def calculate_relative_frequencies(values):
    abs_f = calculate_absolute_frequencies(values)
    f_sum = sum(abs_f.values())
    return {key: value / f_sum for key, value in abs_f.items()}


def calculate_relative_frequencies_and_merge_rare(values, threshold, default_key='OTHER'):
    rel_f = calculate_relative_frequencies(values)
    major_elements = {key: value for key, value in rel_f.items() if value >= threshold}
    minor_f_sum = sum(value for value in rel_f.values() if value < threshold)
    major_elements[default_key] = minor_f_sum
    return major_elements


def format_float_dict(d, precision):
    return {k: round(v, precision) if isinstance(v, float) else v for k, v in d.items()}


def replace_rare_values(items, field, threshold, default_value='OTHER', log=False):
    values = [x[field] for x in items]
    merged_rel_f = calculate_relative_frequencies_and_merge_rare(values, threshold)
    if log:
        print(field, format_float_dict(merged_rel_f, 3))
    for item in items:
        replace_value(item, field, merged_rel_f, default_value=default_value)
    return items


def replace_value(item, field, dictionary, default_value='OTHER'):
    if item[field] not in dictionary:
        item[field] = default_value
    return item


def set_element_first(array, i):
    as_list = list(array)
    element = as_list.pop(i)
    head = [element]
    head.extend(as_list)
    return head


def map_headers_to_data(headers, items):
    return [dict(zip(headers, x)) for x in items]
