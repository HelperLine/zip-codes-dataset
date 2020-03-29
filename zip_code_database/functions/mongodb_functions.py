
from zip_code_database import zip_codes_collection, shapefiles_collection


def format_zip_record_dict(zip_code, city, lat, lng):
    return {
        "zip_code": zip_code,
        "city": city,
        "lat": lat,
        "lng": lng,
        "adjacent_zip_codes": [],
    }

def mongodb_add_zip_record_dict(zip_record_dict):
    zip_codes_collection.insert_one(zip_record_dict)


def mongodb_add_zip_record_dict_batch(zip_record_dict_batch):
    zip_codes_collection.insert_many(zip_record_dict_batch)


def mongodb_get_zip_record_dict(zip_code):
    return zip_codes_collection.find_one({"zip_code": zip_code})


def mongodb_update_zip_record_dict(zip_record_dict):
    zip_codes_collection.update({"zip_code": zip_record_dict["zip_code"]}, {"$set": zip_record_dict})


def mongodb_reset_zip_codes_collection():
    zip_codes_collection.delete_many({})


def mongodb_reset_shapefiles_collection():
    shapefiles_collection.delete_many({})



def format_shape_record_dict(zip_code, shape_list):
    return {
        "zip_code": zip_code,
        "shape_list": shape_list,
    }

def mongodb_add_shape_record_dict(shape_record_dict):
    shapefiles_collection.insert_one(shape_record_dict)

def mongodb_add_shape_record_dict_batch(shape_record_dict_batch):
    shapefiles_collection.insert_many(shape_record_dict_batch)


if __name__ == "__main__":
    # mongodb_reset_zip_codes_collection()
    # mongodb_reset_shapefiles_collection()

    # zip_codes_collection.rename("zip_codes_germany")

    # zip_codes_collection.update_many({}, {"$set": {"agents": 0, "callers": 0}})

    # zip_codes_collection.create_index([('zip_code', pymongo.ASCENDING)], unique=True)

    # shapefiles_collection.create_index([('zip_code', pymongo.ASCENDING)], unique=True)

    pass



