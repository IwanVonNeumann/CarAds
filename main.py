from random import shuffle

import numpy
from sklearn.ensemble import RandomForestRegressor

from analysis.errors import get_abs_errors
from db.mongo_client import c
from transformation.pre_process import pre_process
from utils.utils import extract_keys, extract_values

all_ads = c("ads_raw").find_all()

print("before:", len(all_ads))

preprocessed_data = pre_process(all_ads, log=True)

print("after:", len(preprocessed_data))

max_price = 15000
preprocessed_data = [x for x in preprocessed_data if x["price"] <= max_price]
print("with price < {}: {}".format(max_price, len(preprocessed_data)))

shuffle(preprocessed_data)

feature_names = extract_keys(preprocessed_data)
only_values = extract_values(preprocessed_data)

known = only_values[:11500]
test_records = only_values[11500:12300]

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

print(rfRegressor.feature_importances_)
