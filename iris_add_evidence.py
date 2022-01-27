from unittest import TestCase
from venv import create
import requests
import csv
import json
from requests_toolbelt.utils import dump
import sys

import keys


def add_evidence(cid, filename, file_size, file_hash, file_description):

    if cid > 0:
        iris_data=json.dumps({"filename": filename, "file_size": file_size, "file_hash": file_hash, "file_description": file_description, "cid": cid})
        result = requests.post("{}/case/evidences/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Add evidences to IRIS")
    parser.add_argument("cid", type=int, help="Case ID")
    parser.add_argument("filename", type=str, help="Evidence filename")
    parser.add_argument("file_size", type=int, help="Evidence file size")
    parser.add_argument("file_hash", type=str, help="Evidence file hash (SHA256)")
    parser.add_argument("file_description", type=str, help="Evidence file description")

    args = parser.parse_args()

    add_evidence(args.cid, args.filename, args.file_size, args.file_hash, args.file_description)
        
    print("Evidence {} for case {} added".format(args.filename, args.cid))


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }
    main()
