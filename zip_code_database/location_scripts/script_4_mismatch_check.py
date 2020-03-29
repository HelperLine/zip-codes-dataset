
from zip_code_database import zip_codes_collection, shapefiles_collection

# I have noticed that there are 8180 zip_code_documents and 8179 shapefile_documents
# There should actually be 8178 shapefile_documents because I have manually added two
# zip_code_documents (32351, 32369, see script_1) which did not contain neither a
# location nor a shapelist in the dataset.

print(zip_codes_collection.count_documents({}))
print(shapefiles_collection.count_documents({}))

zip_code_records = list(zip_codes_collection.find({}, {"zip_code": 1}))
shapefile_records = list(shapefiles_collection.find({}, {"zip_code": 1}))

zip_codes_1 = [record["zip_code"] for record in zip_code_records]
zip_codes_2 = [record["zip_code"] for record in shapefile_records]


def get_exclusive_elements(list_1, list_2):
    exclusive_list = []

    for element_1 in list_1:
        if element_1 not in list_2:
            exclusive_list.append(element_1)

    for element_2 in list_2:
        if element_2 not in list_1:
            exclusive_list.append(element_2)

    return exclusive_list


print(get_exclusive_elements(zip_codes_1, zip_codes_2))


# Solution: 98711 has shapelist but multiple location
#       -> no valid GCP geocode response
#       -> deleted record manually from shapefile_documents

