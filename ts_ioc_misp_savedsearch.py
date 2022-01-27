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
        search_obj.name = "IOC search for {} (MISP)".format(ioc)
        search_obj.description = "IOC search for indicator {} coming from MISP".format(ioc)
        search_obj.max_entries = max_entries
        search_obj.save()

        result = search_obj.dict
        if "objects" in result:
            return result["objects"]
        return False
    else:
        return False 


def get_misp_ioc(customer, export_tag_misp):
    misp_data=json.dumps({"returnFormat": "json", "tags": ["customer:{}".format(customer)],"to_ids":"1"})
    indicators=requests.post("{}/attributes/restSearch".format(misp_host), headers=misp_headers, data=misp_data, verify=misp_verify)
    response=indicators.json()["response"]["Attribute"]
    response_attr = []
    for attr in response:
        ioc_tags = ""
        if "Tag" in attr:
            for tag in attr["Tag"]:
                if tag["name"] == export_tag_misp:
                    response_attr.append(attr["value"])
    return response_attr


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fetch events based on a label from TimeSketch and import into case")
    parser.add_argument("sketch_id", type=int, help="TimeSketch ID")
    parser.add_argument("return_fields", type=str, help="TimeSketch fields to return")
    parser.add_argument("customer", type=str, help="MISP customer tag")

    args = parser.parse_args()

    default_return_fields = "message,datetime,timestamp,timestamp_desc,comment"
    default_export_tag_misp = "export:timesketch"
    default_max_entries = 150
    for indicator in get_misp_ioc(args.customer, default_export_tag_misp):
        ts_search_ioc(args.sketch_id,indicator,default_return_fields, args.return_fields, default_max_entries)
        print("Save search for {} added".format(indicator))


if __name__ == "__main__":
    misp_host = keys.misp_host
    misp_apikey = keys.misp_apikey
    misp_headers={"Authorization": misp_apikey, "Accept": "application/json", "Content-Type": "application/json"}
    misp_verify = keys.misp_verify
    main()
