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


def add_sketch_event(sketch_id, message, timestamp, attributes, labels):
    if sketch_id > 0:
        ts_client = config.get_client()
        sketch = ts_client.get_sketch(sketch_id)
        sketch.add_event(message, timestamp, timestamp, attributes, labels)
    else:
        return False 


def main():
    # python ts_add_event.py 10 "2020-08-06T12:48:06.994188Z" '{"abc": "aaa", "o": "omega"}' '["cudeso"]'

    import argparse

    parser = argparse.ArgumentParser(description="Add an event to a TimeSketch")
    parser.add_argument("sketch_id", type=int, help="TimeSketch ID")
    parser.add_argument("timestamp", type=str, help="Timestamp (ISO format)")
    parser.add_argument("attributes", type=str, help="Attributes to add")
    parser.add_argument("labels", type=str, help="Labels to add")

    args = parser.parse_args()
    
    add_sketch_event(args.sketch_id, "blah", args.timestamp, json.loads(args.attributes), json.loads(args.labels))
    print("Event added to sketch {}".format(args.sketch_id))

if __name__ == "__main__":
    main()
