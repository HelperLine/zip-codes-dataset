
from secrets import GCP_API_KEY
import requests
import json


def get_geocode_location(zip_code, city=None, country=None):
    request_url = f"https://maps.googleapis.com/maps/api/geocode/json?" \
                  f"address={zip_code}{'+' + city if city is not None else ''},{country if country is not None else 'Germany'}&" \
                  f"key={GCP_API_KEY}"

    try:
        response = requests.get(request_url)
    except:
        return {"status": "invalid google geocode request"}

    try:
        # print(request_url)
        # print(json.loads(response.text))
        coordinates_dict = json.loads(response.text)["results"][0]["geometry"]["location"]
        result_dict = {
            "status": "ok",
            "lat": coordinates_dict["lat"],
            "lng": coordinates_dict["lng"],
        }
        return result_dict
    except Exception as e:
        # print(e)
        return {"status": "invalid google geocode response"}



