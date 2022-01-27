from unittest import TestCase
from venv import create
import requests
import csv
import json
from requests_toolbelt.utils import dump
import sys

import keys


def create_customer(customer_name):
    client_id = 0
    if customer_name:
        result = requests.get("{}/manage/customers/list".format(iris_host), headers=iris_headers, verify=iris_verify)
        if "data" in result.json():
            for customer in result.json()["data"]:
                if customer['customer_name'] == customer_name:
                    return customer['customer_id']
        
        # No customer found, create one
        iris_data=json.dumps({"customer_name": customer_name})
        result = requests.post("{}/manage/customers/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
        if "data" in result.json() and "customer_id" in result.json()["data"]:
            client_id = result.json()["data"]["customer_id"]
    return client_id


def create_case(case_customer, case_name, case_description="", case_soc_id=""):
    case_id = 0
    if case_customer > 0:
        iris_data=json.dumps({"case_customer": case_customer, "case_name": case_name, "case_description": case_description, "case_soc_id": case_soc_id})
        result = requests.post("{}/manage/cases/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
        if "data" in result.json() and "case_id" in result.json()["data"]:
            case_id = result.json()["data"]["case_id"]
    return case_id


def add_tasks(cid, assignee_id, template, task_status, task_tags):
    if cid > 0:
        with open(template, "rb") as f:
            data = json.load(f)
            tasks = data["tasks"]
            for task in tasks:
                description = ""
                if "description" in task:
                    description = task["description"]
                iris_data=json.dumps({"task_assignee_id": assignee_id, "task_status_id": task_status, "task_title": task["title"], "task_description": description, "task_tags": task_tags, "cid": cid})
                result = requests.post("{}/case/tasks/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
                #print(result.text)


def add_global_task(cid, name, customer, assignee_id, task_status, task_tags):
    if cid > 0:
        task_title = "Address the new case '{}' for {}".format(name, customer)
        task_description = ""
        iris_data=json.dumps({"task_assignee_id": assignee_id, "task_status_id": task_status, "task_title": task_title, "task_description": task_description, "task_tags": task_tags})
        result = requests.post("{}/global/tasks/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
        #print(result.text)


def add_notes(cid, name, customer):
    notes = {}  
    f_notes = open("notes_intake.md")
    notes["intake"] = f_notes.read()
    f_notes.close()

    notes["live-forensics"] = "Live forensics"
    notes["ir-pi-setup"] = "IR PI Setup details"
    notes["evidences"] = "Evidences"

    if cid > 0:
        add_notes_helper(cid, "Intake", "Customer {} contact details".format(customer), notes["intake"])
        add_notes_helper(cid, "Live Forensics", "Assets".format(customer), notes["live-forensics"])
        add_notes_helper(cid, "Tooling", "IR-PI".format(customer), notes["ir-pi-setup"])


def add_notes_helper(cid, group_title, note_title, note_content):
    if cid > 0:
        iris_data=json.dumps({"group_title": group_title, "cid": cid})
        result = requests.post("{}/case/notes/groups/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)
        if "data" in result.json():
            group_id = result.json()["data"]["group_id"]
            iris_data=json.dumps({"note_title": note_title, "note_content": note_content, "group_id": group_id, "cid": cid})
            result = requests.post("{}/case/notes/add".format(iris_host), headers=iris_headers, data=iris_data, verify=iris_verify)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bootstap a case in DFIR-IRIS")
    parser.add_argument("customer", type=str, help="Customer name. Customers are automatically added if they don't exist.")
    parser.add_argument("casetemplate", type=str, help="TheHive template to use as case template for tasks")
    parser.add_argument("name", type=str, help="Case name")
    parser.add_argument("description", type=str, help="Case description")
    args = parser.parse_args()

    default_soc_ticket = ""
    default_assignee_id = 1
    default_task_status = 1
    default_task_tags = ""

    customer_id = create_customer(args.customer)
    cid = create_case(customer_id, args.name, args.description, default_soc_ticket)
    add_tasks(cid, default_assignee_id, args.casetemplate, default_task_status, default_task_tags)
    add_global_task(cid, args.name, args.customer, default_assignee_id, default_task_status, "case_mgmnt")
    add_notes(cid, args.name, args.customer)
    
    print("Case {} created".format(cid))


if __name__ == "__main__":
    iris_host = keys.iris_host
    iris_apikey = keys.iris_apikey
    iris_verify = keys.iris_verify
    iris_headers = {"Authorization": "Bearer {}".format(iris_apikey), "Content-Type": "application/json" }
    main()
