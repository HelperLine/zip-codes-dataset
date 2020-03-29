
from pymongo import MongoClient
from secrets import MONGODB_CONNECTION_STRING


# Setting correct SSL Certificate path
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()


client = MongoClient(MONGODB_CONNECTION_STRING)
database = client.get_database("zip_codes")
zip_codes_collection = database.zip_codes_germany
shapefiles_collection = database.zip_codes_germany_shapefiles


