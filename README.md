# dfir-iris-misp-timesketch
Scripts to integrate DFIR-IRIS, MISP and TimeSketch

![dfir.drawio.png](/dfir.drawio.png)

## Usage and Scripts

### MISP

#### Event
*  First start by creating a **new MISP threat event**
*  Add all the artefacts that you investigated
*  * Malware samples
*  * * [Upload the samples to MWDB-core](https://www.vanimpe.eu/2021/12/27/send-malware-samples-from-misp-to-mwdb-malware-repository/)
*  * * [Upload the samples to VMRay](https://www.vanimpe.eu/2019/05/07/submit-malware-samples-to-vmray-via-misp-automation/)
*  * E-mails 
*  * Other relevant documents
*  * Store samples in secure storage
*  * Add MISP reports
*  * Get text from to web pages
* * Add IOCs

#### Custom taxonomy
* Make sure you have a custom taxonomy (or custom tags) that consists of the "customer:<customer-name>". You can use another prefix but then you have to change the script(s).

![misp-tag-customer.jpg](misp-tag-customer.jpg)


### VENV

* Enter Python virtual environment
* * See [pip-venv-list.txt](pip-venv-list.txt)
* `source timesketch_api/bin/activate``

### IRIS

#### Use iris_create_case.py

As a second step create the case in IRIS.

```
(timesketch_api) user@timesketch:~/demo/scripts$ python iris_create_case.py -h
usage: iris_create_case.py [-h] customer casetemplate name description

Bootstap a case in DFIR-IRIS

positional arguments:
  customer      Customer name. Customers are automatically added if they don't exist.
  casetemplate  TheHive template to use as case template for tasks
  name          Case name
  description   Case description

optional arguments:
  -h, --help    show this help message and exit
(timesketch_api) user@timesketch:~/demo/scripts$ python iris_create_case.py demo ../data/thehive.json "My Demo case" "My Demo Description"
Case 12 created
```

* This script creates a new IRIS case
* Adds a default set of notes, based on MD templates (such as "notes_intake.md")
* Adds default set of tasks, based on a TheHive template
* Adds a global task

![iris-create_case.jpg](iris-create_case.jpg)

The list of tasks comes from TheHive template, such as for example the file [thehive.json](thehive.json)

#### iris_delete_tasks.py

The script iris_delete_tasks.py deletes the tasks of a specific case.

```
(timesketch_api) user@timesketch:~/demo/scripts$ python iris_delete_tasks.py -h
usage: iris_delete_tasks.py [-h] cid

Delete tasks

positional arguments:
  cid         Case ID

optional arguments:
  -h, --help  show this help message and exit

(timesketch_api) user@timesketch:~/demo/scripts$ python iris_delete_tasks.py 11
{'data': [], 'message': 'Task deleted', 'status': 'success'}
{'data': [], 'message': 'Task deleted', 'status': 'success'}
{'data': [], 'message': 'Task deleted', 'status': 'success'}
{'data': [], 'message': 'Task deleted', 'status': 'success'}
{'data': [], 'message': 'Task deleted', 'status': 'success'}
{'data': [], 'message': 'Task deleted', 'status': 'success'}
{'data': [], 'message': 'Task deleted', 'status': 'success'}
Tasks for case 11 deleted  
```

* Delete tasks from an IRIS case

#### iris_add_assets.py

As a third step import the asset lists you worked on. The asset list is stored in CSV format. 

`asset_name, asset_type_id, asset_description, asset_domain, asset_ip, asset_info, analysis_status_id, asset_compromised`

* Add assets to IRIS from a CSV file

```
(timesketch_api) user@timesketch:~/demo/scripts$ python iris_add_assets.py -h
usage: iris_add_assets.py [-h] cid csv

Add assets from CSV file to a case

positional arguments:
  cid         Case ID
  csv         Location of CSV file

optional arguments:
  -h, --help  show this help message and exit

(timesketch_api) user@timesketch:~/demo/scripts$ python iris_add_assets.py 12 ../data/assets.csv
Assets for case 12 added
```

#### iris_add_evidence.py
* Add evidence to IRIS

#### iris_get_from_ts.py
* Get Timeline events from TimeSketch

#### iris_add_iocs_misp.py
* Add IOCs from MISP to IRIS



#### iris_get_from_ts_savedsearch.py
* Get timeline events from a Timesketch saved search

#### iris_get_from_ts_savedsearch_byid.py
* Get timeline events from a TimeSketch saved search (by id)

### TimeSketch

#### ts_import_pcap.py
* Import PCAP file into TimeSketch 

#### ts_ioc_iris_savedsearch.py
* Create a saved search based on IOCs in an IRIS case

#### ts_add_event.py
* Manually add a TimeSketch event

#### ts_ioc_misp_savedsearch.py
* Create a saved search based on IOCs from a MISP event

##### ts_create_sketch.py
* Create a TimeSketch sketch

#### ts_import_evtx.py
Import EVTX file into TimeSketch

# Elastic

[https://github.com/cudeso/elastic-dfir-cluster](https://github.com/cudeso/elastic-dfir-cluster)
