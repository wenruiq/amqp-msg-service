#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from datetime import datetime
import json
import pika

import hashlib
import hmac
import base64
from urllib.parse import urlencode, urlparse

# from signature import process_url

app = Flask(__name__)

CORS(app)

app.config["GMAPS_API_KEY"] = os.environ.get("GMAPS_API_KEY")
app.config["GPLACES_API_KEY"] = os.environ.get("GPLACES_API_KEY")
app.config["URL_SIGNING_SECRET"] = os.environ.get("URL_SIGNING_SECRET")
maps_key = app.config["GMAPS_API_KEY"]
places_key = app.config["GPLACES_API_KEY"]
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/location/search/<string:location>", methods=["GET"])
def search(location):
    autocomplete_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={location}&key={places_key}&types[]=address&types[]=establishments"
    place_autocomplete = json.loads(requests.get(autocomplete_url).text)
    location_list = []

    for location in place_autocomplete["predictions"]:
        # retrieve place id and place description
        # send request for place details and get formatted_address
        # put in dict and append to a list
        place_id = location["place_id"]
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address,geometry&key={places_key}"
        r = requests.get(details_url)
        result = json.loads(r.text)["result"]
        address = result["formatted_address"]
        location_json = {
            "description": location["description"],
            "place_id": place_id,
            "address": address
            }
        location_list.append(location_json)
    location_dict = {"predictions": location_list}
    return location_dict

@app.route("/location/static-map/<string:place_id>", methods=["GET"])
def get_static_map(place_id):

    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address,geometry&key={places_key}"
    r = requests.get(details_url)
    result = json.loads(r.text)["result"]
    address = result["formatted_address"]
    lat = result["geometry"]["location"]["lat"]
    lng = result["geometry"]["location"]["lng"]

    map_parameters = {
        "size": "200x150",
        "markers": f"color:red|{str(lat)},{str(lng)}",
        "key": maps_key
    }
    search_parameters = {
        "query": address,
        "query_place_id": place_id
    }

    map_url = "https://maps.googleapis.com/maps/api/staticmap?" + urlencode(map_parameters)
    map_url = process_url(map_url, app.config["URL_SIGNING_SECRET"])
    search_url = "https://www.google.com/maps/search/?api=1&" + urlencode(search_parameters)
    return f"<img src='{map_url}'><br><a href='{search_url}' target='_blank'>{address}</a>"

def process_url(input_url, signing_secret):
  """ Signs a URL using a URL signing secret """
  url = urlparse(input_url)
  url_to_sign = url.path + "?" + url.query
  decoded_key = base64.urlsafe_b64decode(signing_secret)
  signature = hmac.new(decoded_key, url_to_sign.encode("utf-8"), hashlib.sha1)
  encodedSignature = base64.urlsafe_b64encode(signature.digest()).decode('ascii')
  original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query
  full_url = original_url + "&signature=" + encodedSignature
  return full_url

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9003, debug=True)