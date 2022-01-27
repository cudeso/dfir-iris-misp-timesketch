from unittest import TestCase
from venv import create
import requests
import csv
import json
from requests_toolbelt.utils import dump
import sys

import keys


def delete_tasks(cid):
    if cid > 0:
        result = requests.get("{}/case/tasks/list?cid={}".format(iris_host, cid), headers=iris_headers, verify=iris_verify)
        if "data" in result.json() and "tasks" in result.json()["data"]:
            for task in result.json()["data"]["tasks"]:
                task_id = task["task_id"]
                result_delete = requests.get("{}/case/tasks/delete/{}?cid={}".format(iris_host, task_id, cid), headers=iris_headers, verify=iris_verify)
                print(result_delete.json())


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Delete tasks")
    parser.add_argument("cid", type=int, help="Case ID")
    args = parser.parse_args()

    delete_tasks(args.cid)    
    print("Tasks for case {} deleted".format(args.cid))


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }    
    main()
