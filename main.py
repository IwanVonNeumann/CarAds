from db.mongo_client import c
from transformation.pre_process import pre_process
from utils.utils import feature_unique_values

all_ads = c("ads_raw").find_all()

print("before:", len(all_ads))

nice_data = pre_process(all_ads, log=True)

print("after:", len(nice_data))

unique_transmission = feature_unique_values(nice_data, "transmission")

print(unique_transmission)
print(len(unique_transmission))
