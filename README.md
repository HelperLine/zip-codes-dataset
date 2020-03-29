
## Zip-Code Database on MongoDB Atlas

The database is based on this dataset: https://public.opendatasoft.com/explore/dataset/postleitzahlen-deutschland/information/

For some zip-codes I used the Google Geocode API.

<br/>

### Zip-Code Collection

I created a MongoDB database containing all german household zip-codes as well 
as all the adjacent zip-codes with their respective distance.

This is how the database records look like:
```json
{
    "_id": {"$oid": "..."},
    "zip_code": "61476",
    "city": "Kronberg im Taunus",
    "lat": {"$numberDouble": "50.1887724"},
    "lng": {"$numberDouble": "8.5159547"},
    "adjacent_zip_codes": [
        {
            "zip_code": "65824",
            "distance": {"$numberDouble": "4.5512419"}
        }, {
            "zip_code": "61440",
            "distance": {"$numberDouble": "4.9010408"}
        }, {
            "zip_code": "65812",
            "distance": {"$numberDouble": "5.2619112"}
        }, {
            "zip_code": "61462",
            "distance": {"$numberDouble": "6.0350328"}
        }, {
            "zip_code": "61449",
            "distance": {"$numberDouble": "6.385412"}
        }
    ]
}
```

The `adjacent_zip_codes`-list contains at most 20 zip-codes and only zip-codes less 
than 25km away. The list is already sorted ascendingly.

*These parameters can easily be changed (See `scripts/script_2_compute_distances.py`).* 

<br/>

There are 379 zip-code-regions in the dataset which are made up of more than one 
distinct region. For these duplicate zip-code-regions I used google geocode to 
determine a proper center (See `scripts/script_1_insert_zip_records.py`).


### Zip-Code-Region Shape-File Collection

I also added one collection containing all shape-files for the zip-code-regions.

The documents look like this:

```json
{
    "_id": {"$oid": "..."},
    "zip_code": "61476",
    "shape_list": [
        [
            [{"$numberDouble": "8.4746763"}, {"$numberDouble": "50.2070396"}],
            [{"$numberDouble": "8.4756335"}, {"$numberDouble": "50.2081467"}],
            [{"$numberDouble": "8.4818554"}, {"$numberDouble": "50.2072468"}],
            [{"$numberDouble": "8.4865283"}, {"$numberDouble": "50.2090631"}],
            [{"$numberDouble": "8.4838984"}, {"$numberDouble": "50.2099904"}],
            [{"$numberDouble": "8.4829493"}, {"$numberDouble": "50.2101142"}],
            [{"$numberDouble": "8.4791487"}, {"$numberDouble": "50.211628"}]
        ]
    ]
```

The `shape_list` is an array of array of lat-lng-tuples because of the 379 
zip-code-regions which are made up of more than one distinct region.

For these I store all respective region-shapes.

One shape can easily contain hundreds of vertices.

(See `scripts/script_3_store_shapefiles.py`)

<br/>

### Personal MongoDB documentation

This project was partly meant to learn MongoDB (Atlas).

See my personal documentation of their python API `pymongo` in `notebooks`.