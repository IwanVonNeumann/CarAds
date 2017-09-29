from random import shuffle

import numpy
from sklearn.ensemble import RandomForestRegressor

from analysis.stats import get_abs_errors, get_combined_feature_importances
from db.mongo_client import c
from transformation.pre_process import pre_process
from transformation.transform import split_features, remove_rare_models
from utils.formatting import freq_dict_to_percent_dict
from utils.utils import sort_dict

all_ads = c("ads_raw").find_all()

print("before:", len(all_ads))

preprocessed_data = pre_process(all_ads, log=True)

# preprocessed_data = remove_rare_models(preprocessed_data, 1)

print("after:", len(preprocessed_data))

split_data = split_features(preprocessed_data, key_feature="price", log=True)

feature_names = split_data["feature_names"]
only_values = split_data["data"]

shuffle(only_values)

known = only_values[:14500]
test_records = only_values[14500:15400]

problem = [x[1:] for x in test_records]
answer = [x[0] for x in test_records]

target = [x[0] for x in known]
train = [x[1:] for x in known]

rfRegressor = RandomForestRegressor(n_estimators=100)
rfRegressor.fit(train, target)

prediction = rfRegressor.predict(problem)

errors = get_abs_errors(prediction, answer)

print(errors)
print(numpy.mean([abs(error) for error in errors]))

feature_importances = get_combined_feature_importances(feature_names[1:], rfRegressor.feature_importances_)

formatted_feature_importances = freq_dict_to_percent_dict(feature_importances)

sorted_feature_importances = sort_dict(feature_importances)

for x in sorted_feature_importances:
    print(x)
