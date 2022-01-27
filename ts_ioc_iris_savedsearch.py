from asyncio import format_helpers
from timesketch_api_client import config
from timesketch_api_client import search
import requests
import csv
import json
from requests_toolbelt.utils import dump
from datetime import datetime

import sys

import keys


def ts_search_ioc(sketch_id, ioc, default_return_fields, return_fields, max_entries):
    if sketch_id > 0:
        ts_client = config.get_client()
        sketch = ts_client.get_sketch(sketch_id)
        search_obj = search.Search(sketch=sketch)

        search_obj.query_string = ioc

        if return_fields:
            return_fields = "{},{}".format(default_return_fields, return_fields)
        else:
            return_fields = default_return_fields
        search_obj.return_fields = return_fields
        search_obj.name = "IOC search for {} (IRIS)".format(ioc)
        search_obj.description = "IOC search for indicator {} coming from IRIS".format(ioc)
        search_obj.max_entries = max_entries
        search_obj.save()

        result = search_obj.dict
        if "objects" in result:
            return result["objects"]
        return False
    else:
        return False 


def get_iris_ioc(cid):
    response_attr = []
    if cid > 0:
        result = requests.get("{}/case/ioc/list?cid={}".format(iris_host, cid), headers=iris_headers, verify=iris_verify)
        if "data" in result.json():
            for attr in result.json()["data"]["ioc"]:
                response_attr.append(attr["ioc_value"])
    return response_attr


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Create a saved search on basis of IOCs in IRIS")
    parser.add_argument("sketch_id", type=int, help="TimeSketch ID")
    parser.add_argument("return_fields", type=str, help="TimeSketch fields to return")
    parser.add_argument("cid", type=int, help="IRIS Case ID")


    args = parser.parse_args()

    default_return_fields = "message,datetime,timestamp,timestamp_desc,comment"
    default_max_entries = 150
    for indicator in get_iris_ioc(args.cid):
        ts_search_ioc(args.sketch_id,indicator,default_return_fields, args.return_fields, default_max_entries)
        print("Save search for {} added".format(indicator))


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }
    main()
