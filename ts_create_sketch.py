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


def create_sketch(name, description):
    if name:
        ts_client = config.get_client()
        sketch = ts_client.create_sketch(name, description)
        return sketch.id
    else:
        return False 


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Create a new TimeSketch")
    parser.add_argument("name", type=str, help="TimeSketch name")
    parser.add_argument("description", type=str, help="TimeSketch description")
    args = parser.parse_args()
    print("Sketch {} created".format(create_sketch(args.name,args.description)))


if __name__ == "__main__":
    main()
