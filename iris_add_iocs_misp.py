from unittest import TestCase
from venv import create
import requests
import csv
import json
from requests_toolbelt.utils import dump
import sys

import keys



def add_iocs(cid, customer, iris_ioc, export_tag_misp):

    default_tlp_code = 2

    misp_data=json.dumps({"returnFormat": "json", "tags": ["customer:{}".format(customer)],"to_ids":"1"})
    indicators=requests.post("{}/attributes/restSearch".format(misp_host), headers=misp_headers, data=misp_data, verify=misp_verify)
    response=indicators.json()["response"]["Attribute"]
    for attr in response:
        ioc_tags = ""
        value=attr["value"]
        if 'Tag' in attr:
            for t in attr["Tag"]:
                if t["name"] == export_tag_misp:
                    # Double loop; now add the tags
                    for t2 in attr["Tag"]:
                        if t["name"] != export_tag_misp:
                            ioc_tags += t["name"] + ","

                    attr_type=attr["type"]

                    iris_attr_type = match_iris_ioc(iris_ioc, attr_type)
                    iris_data=json.dumps({"ioc_type_id": iris_attr_type, "ioc_tlp_id": default_tlp_code, "ioc_value": value, "ioc_description": "From MISP", "ioc_tags": ioc_tags, "cid": cid})
                    result = requests.post("{}/case/ioc/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
                    #print(result.text)        


def get_ioc_types():
    result = requests.get("{}/manage/ioc-types/list".format(iris_host), headers=iris_headers, verify=iris_verify)
    if "data" in result.json():
        return result.json()["data"]
    else:
        return False


def match_iris_ioc(iris_ioc, match):
    if iris_ioc:
        for el in iris_ioc:
            if el["type_name"] == match:
                return el["type_id"]
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Add IOCs from MISP")
    parser.add_argument("cid", type=int, help="Case ID")
    parser.add_argument("customer", type=str, help="Case ID")
    args = parser.parse_args()

    default_export_tag_misp = "export:iris"

    iris_ioc = get_ioc_types()
    if iris_ioc:
        add_iocs(args.cid, args.customer, iris_ioc, default_export_tag_misp)
        
    print("IOCs for case {} added".format(args.cid))


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }
    misp_host = keys.misp_host
    misp_apikey = keys.misp_apikey
    misp_headers={"Authorization": misp_apikey, "Accept": "application/json", "Content-Type": "application/json"}
    misp_verify = keys.misp_verify
    main()
