from transformation.remove_incomplete import remove_incomplete
from transformation.transform import transform_fields


def pre_process(items, log=False):
    items = remove_incomplete(items, log=log)
    items = transform_fields(items, log=log)
    return items
