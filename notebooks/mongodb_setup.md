# MongoDB Setup

Quick Setup for MongoDB Atlas - Moritz Makowski

<br/>

## 1) Cloud Setup

**1. Log in** at https://cloud.mongodb.com/

**2. Create Cluster**

**3. Create Cluster-User-Identity** under [Security -> Database Access -> Add New Database User]

**4. Whitelist specific IP's** under [Security -> Network Access -> Add IP Address]

**5. Get your connection string** under [Clusters -> Connect -> Connect Your Application -> Python]

<br/>

## 2) Application Setup


```python

# Set correct SSL certificate

import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

```


```python

# connect to your cluster

from secrets import MONGODB_CONNECTION_STRING
from pymongo import MongoClient

client = MongoClient(MONGODB_CONNECTION_STRING)

# This is the string you got in Step 1.5 . Remember to
# insert the username and passwort you created in Step 1.3

```


```python

# connect to your database/collection

database = client.get_database("notebook_database")  # my example database name
collection = database["notebook_collection"]         # my example collectio name inside that database

```


```python

# count documents in collection
# you can pass a filter object to this function

collection.count_documents({})

```




    0



<br/>

## 3) Inserting


```python

# insert one record

new_person = {
    "name": "Peter",
    "happy": True
}


collection.insert_one(new_person)

collection.count_documents({})

```




    1




```python

# insert many records at once

new_people = [
    {
        "name": "Mary",
        "happy": True
    },{
        "name": "Paul",
        "happy": False
    },{
        "name": "Ann",
        "happy": False
    },{
        "name": "Martin",
        "happy": True
    }
]

collection.insert_many(new_people)

collection.count_documents({})

```




    5



<br/>

## 4) Deleting


```python

# delete one record (the first one matching the filter)

collection.delete_many({"name": "Mary"})

collection.count_documents({})

```




    4




```python

# delete many records (all the ones matching the filter)

collection.delete_many({"happy": True})

collection.count_documents({})

```




    2




```python

# Empty the whole collection

collection.delete_many({})

collection.count_documents({})

```




    0




```python

# Restoring the documents for further examples

new_people = [
    {
        "name": "Mary",
        "happy": True
    },{
        "name": "Paul",
        "happy": False
    },{
        "name": "Ann",
        "happy": False
    },{
        "name": "Martin",
        "happy": True
    }
]

collection.insert_many(new_people)

collection.count_documents({})

```




    4



<br/>

## 5) Querying


```python

# Find one record

collection.find_one({"happy": True})

```




    {'_id': ObjectId('5e8084a9d4282bdc82418eec'), 'name': 'Mary', 'happy': True}




```python

# Find many records

list(collection.find({"happy": True}))

```




    [{'_id': ObjectId('5e8084a9d4282bdc82418eec'), 'name': 'Mary', 'happy': True},
     {'_id': ObjectId('5e8084a9d4282bdc82418eef'),
      'name': 'Martin',
      'happy': True}]




```python

# include specific fields - this is called "projection"

list(collection.find({"happy": True}, {"name": 1}))

```




    [{'_id': ObjectId('5e8084a9d4282bdc82418eec'), 'name': 'Mary'},
     {'_id': ObjectId('5e8084a9d4282bdc82418eef'), 'name': 'Martin'}]




```python
# excluse specific fields - this is called "projection"

list(collection.find({"happy": True}, {"_id": 0}))

```




    [{'name': 'Mary', 'happy': True}, {'name': 'Martin', 'happy': True}]




```python

# You cannot mix inclusions and exclusion

from pymongo.errors import OperationFailure

try:
    list(collection.find({"happy": True}, {"happy": 0, "name": 1}))
except OperationFailure as e:
    print(f"OperationFailure: {e}")

```

    OperationFailure: Projection cannot have a mix of inclusion and exclusion.


<br/>

## 6) Updating


```python

# Update one record

collection.update_one({"name": "Ann"}, {"$set": {"happy": True}})

list(collection.find({"happy": True}, {"_id": 0}))

```




    [{'name': 'Mary', 'happy': True},
     {'name': 'Ann', 'happy': True},
     {'name': 'Martin', 'happy': True}]




```python

# Update many records

collection.update_many({"happy": True}, {"$set": {"happy": False}})

print(list(collection.find({"happy": True}, {"_id": 0})))
print(list(collection.find({"happy": False}, {"_id": 0})))

```

    []
    [{'name': 'Mary', 'happy': False}, {'name': 'Paul', 'happy': False}, {'name': 'Ann', 'happy': False}, {'name': 'Martin', 'happy': False}]



```python
# Restoring the documents for further examples

collection.delete_many({})

new_people = [
    {
        "name": "Mary",
        "happy": True
    },{
        "name": "Paul",
        "happy": False
    },{
        "name": "Ann",
        "happy": False
    },{
        "name": "Martin",
        "happy": True
    }
]

collection.insert_many(new_people)

collection.count_documents({})

```




    4



<br/>

## 7) Bulk Operations


```python

# Combine multiple operations into one request

from pymongo.errors import BulkWriteError
from pymongo import InsertOne, UpdateOne, DeleteOne

operations = [
    InsertOne({"name": "Marcus", "happy": True}),
    UpdateOne({"name": "Ann"}, {"$set": {"happy": True}}),
    DeleteOne({"name": "Mary"})
]

collection.bulk_write(operations, ordered=True)

list(collection.find({}, {"_id": 0}))

```




    [{'name': 'Paul', 'happy': False},
     {'name': 'Ann', 'happy': True},
     {'name': 'Martin', 'happy': True},
     {'name': 'Marcus', 'happy': True}]



<br/>

## 8) Indexes

**Benefits:**
* More performant queries when using the index as a filter-parameter
* Possibility to define fields that have to be unique


```python

# Create an index

import pymongo

collection.create_index([('name', pymongo.ASCENDING)], unique=True)

```




    'name_1'




```python

# Now when trying to insert a record with an already existing value in a unique field, it fails

from pymongo.errors import DuplicateKeyError

try:
    collection.insert_one({"name": "Paul", "happy": True})
except DuplicateKeyError as e:
    print(f"DuplicateKeyError: {e}")

```

    DuplicateKeyError: E11000 duplicate key error collection: notebook_database.notebook_collection index: name_1 dup key: { name: "Paul" }



```python

# See: nothing has been changed

list(collection.find({}, {"_id": 0}))

```




    [{'name': 'Paul', 'happy': False},
     {'name': 'Ann', 'happy': True},
     {'name': 'Martin', 'happy': True},
     {'name': 'Marcus', 'happy': True}]



Indexes are fully transparent - so whether or not you use indexes does not change anything about the query syntax!

<br/>

## 9) Collection Settings


```python

# renaming a collection

collection.rename("notebook_collection_example")

```




    {'ok': 1.0,
     '$clusterTime': {'clusterTime': Timestamp(1585482625, 2),
      'signature': {'hash': b'\x90-\xc4\xe3|\x0b}&\xbfd\tA\xd4"S\x11\x86K\x10\xef',
       'keyId': 6807860005560123394}},
     'operationTime': Timestamp(1585482625, 2)}




```python

# do operations still work on the collection object?

collection.count_documents({})

```




    0




```python

# No! We have to redefine the collection object

collection = database["notebook_collection_example"]

collection.count_documents({})

```




    4




```python

# renaming it back

collection.rename("notebook_collection")

collection = database["notebook_collection"]

collection.count_documents({})

```




    4


