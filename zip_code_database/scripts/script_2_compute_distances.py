
from pymongo.errors import BulkWriteError
from pymongo import UpdateOne

from zip_code_database import zip_codes_collection

from pprint import pprint

import math
from tqdm import tqdm

earth_circumference = 40030  # in km


# For each zip_code compute all adjacent zip_codes which are less than 25 km away
# Store at most 20 adjacent zip_codes. We don't have to use these numbers just
# because they are in the database. But these should be a good tradeoff between
# performance and match-quality

# On my machine the whole brute-forcing of 8180 zip_codes takes about 150 seconds,
# so optimizing is not worth the effort!


def get_distance(record_1, record_2):
    # result in km
    # Since we only car about distances < +-25 km we don't have to evaluate the
    # distance on a sphere (https://en.wikipedia.org/wiki/Great-circle_distance)
    # and can just use the way faster pythogoras. The zip_code lat/lng is an
    # average anyway.

    lat_distance = (abs(record_1["lat"] - record_2["lat"])/360.0) * earth_circumference
    lng_distance = (abs(record_1["lng"] - record_2["lng"])/360.0) * earth_circumference

    return round(math.sqrt(math.pow(lat_distance, 2) + math.pow(lng_distance, 2)), 7)


records = list(zip_codes_collection.find({}))

# post updates in batches of 100 records
update_requests_batch = []

for record_1 in tqdm(records):

    adjacent_zip_codes = []

    for record_2 in records:
        if record_1["zip_code"] != record_2["zip_code"]:
            distance = get_distance(record_1, record_2)

            if distance < 25:
                adjacent_zip_codes.append({"zip_code": record_2["zip_code"], "distance": distance})


    adjacent_zip_codes.sort(key=(lambda x: x["distance"]))

    if len(adjacent_zip_codes) > 20:
        adjacent_zip_codes = adjacent_zip_codes[0: 20]

    update_requests_batch.append(UpdateOne({"zip_code": record_1["zip_code"]}, {"$set": {"adjacent_zip_codes": adjacent_zip_codes}}))

    if len(update_requests_batch) == 100:
        try:
            zip_codes_collection.bulk_write(update_requests_batch, ordered=False)
            update_requests_batch = []
        except BulkWriteError as bwe:
            pprint(bwe.details)
            exit()


if len(update_requests_batch) != 0:
    zip_codes_collection.bulk_write(update_requests_batch, ordered=False)
