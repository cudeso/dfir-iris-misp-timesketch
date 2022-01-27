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


def ts_search_chip(sketch_id, label, default_return_fields, return_fields):
    if sketch_id > 0:
        ts_client = config.get_client()
        sketch = ts_client.get_sketch(sketch_id)
        search_obj = search.Search(sketch=sketch)
        if return_fields:
            return_fields = "{},{}".format(default_return_fields, return_fields)
        else:
            return_fields = default_return_fields
        search_obj.return_fields = return_fields
        label_chip = search.LabelChip()
        label_chip.label = label
        search_obj.add_chip(label_chip)
        result = search_obj.dict
        if "objects" in result:
            return result["objects"]
        return False
    else:
        return False 


def add_notes_helper(cid, group_title, note_title, note_content):
    if cid > 0:
        iris_data=json.dumps({"group_title": group_title, "cid": cid})
        result = requests.post("{}/case/notes/groups/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
        if "data" in result.json():
            group_id = result.json()["data"]["group_id"]
            iris_data=json.dumps({"note_title": note_title, "note_content": note_content, "group_id": group_id, "cid": cid})
            result = requests.post("{}/case/notes/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)


def get_asset_id(cid, asset_name):
    if cid > 0:
        result = requests.get("{}/case/assets/list?cid={}".format(iris_host, cid), headers=iris_headers, verify=iris_verify)
        if "data" in result.json():
            for asset in result.json()["data"]["assets"]:
                if asset["asset_name"] == asset_name:
                    return asset["asset_id"]
        return 0


def add_evidence(cid, evidence, label, default_return_fields):
    if cid > 0:
        note_evidence = "|Timestamp|Message|Comment|Fields|ID|\n|---------|-------|-------|------|--|"
        for ev in evidence:
            field_line = ""
            asset = 0
            for field in ev["_source"]:
                if field == 'Computer':
                    asset = int(get_asset_id(cid, ev["_source"]["Computer"], "asset_name"))
                if field == 'src_ip':
                    asset = int(get_asset_id(cid, ev["_source"]["src_ip"], "asset_ip"))

                event_assets = []
                if asset > 0:
                    event_assets = [asset]
                if field not in default_return_fields and field != "label":
                    field_line = "{} {}".format(field_line, "{}= {} ".format(field, ev["_source"][field]))
            line = "|{}|{}| {} |{}|{}|".format(ev["_source"]["timestamp"], ev["_source"]["message"], ev["_source"]["comment"], field_line, ev["_id"])
            note_evidence = "{}\n{}".format(note_evidence, line)

            default_event_colour = "#1572E899"
            timestamp_divider = 1000000
            event_date = datetime.fromtimestamp(int(ev["_source"]["timestamp"]) / timestamp_divider).isoformat(timespec="microseconds")
            event_tz = "+00:00"            
            event_category_id = 1
            iris_data=json.dumps({"event_color": default_event_colour, "event_title": ev["_source"]["message"], "event_content": line, "event_raw": line, "event_source": label, "event_assets": event_assets, "event_category_id": event_category_id, "event_date": event_date, "event_tz": event_tz, "event_in_graph": True, "event_in_summary": True,  "event_tags": "timesketch",  "cid": cid })
            result = requests.post("{}/case/timeline/events/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)

            print("Adding events to timeline {}".format(ev["_source"]["message"]))
        add_notes_helper(cid, "Evidences", label, note_evidence )
        print("Note added")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fetch events based on a label from TimeSketch and import into case")
    parser.add_argument("sketch_id", type=int, help="TimeSketch ID")
    parser.add_argument("label", type=str, help="TimeSketch Label (chip")
    parser.add_argument("return_fields", type=str, help="TimeSketch Fields to return")
    parser.add_argument("cid", type=int, help="IRIS Case ID")
    args = parser.parse_args()

    default_return_fields = "message,datetime,timestamp,timestamp_desc,comment"
    result = ts_search_chip(args.sketch_id, args.label, default_return_fields, args.return_fields)
    if result:        
        add_evidence(args.cid, result, args.label, default_return_fields)
        print("Events added")


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }    
    main()
