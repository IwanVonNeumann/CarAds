def get_abs_errors(x, y):
    n = len(x)
    return [x[i] - y[i] for i in range(0, n)]


def get_feature_importances(names, importances):
    return dict(zip(names, importances))


def get_combined_feature_importances(names, importances):
    feature_importances = get_feature_importances(names, importances)

    combined_feature_importances = {}

    split_features = ["model", "color", "city", "engine_type", "body_type", "transmission"]

    for key in feature_importances.keys():
        key_base = key.split("=")[0]
        if key_base in split_features:
            cum_value = combined_feature_importances.get(key_base)
            if cum_value is None:
                cum_value = 0
            cum_value += feature_importances[key]
            combined_feature_importances[key_base] = cum_value
        else:
            combined_feature_importances[key] = feature_importances[key]

    return combined_feature_importances
