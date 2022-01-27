from unittest import TestCase
from venv import create
import requests
import csv
import json
from requests_toolbelt.utils import dump
import sys

import keys


def add_assets(cid, assetfile):
    if cid > 0:
        with open(assetfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                iris_data=json.dumps({"asset_name":row[0], "asset_type_id": row[1], "asset_description": row[2], "asset_domain": row[3], "asset_ip": row[4], "asset_info": row[5], "analysis_status_id": row[6], "asset_compromised": row[7], "cid": cid})
                result = requests.post("{}/case/assets/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
                #print(dump.dump_all(result))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Add assets from CSV file to a case")
    parser.add_argument("cid", type=int, help="Case ID")
    parser.add_argument("csv", type=str, help="Location of CSV file")
    args = parser.parse_args()

    add_assets(args.cid, args.csv)
    print("Assets for case {} added".format(args.cid))


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }    
    main()
