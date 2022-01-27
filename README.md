# dfir-iris-misp-timesketch
Scripts to integrate DFIR-IRIS, MISP and TimeSketch

![dfir.drawio.png](/dfir.drawio.png)

## Scripts

### IRIS

#### iris_create_case.py
* Create a new IRIS case
* Add default set of notes, based on MD templates (such as "notes_intake.md")
* Add default set of tasks, based on a TheHive template
* Add global task

#### iris_delete_tasks.py
* Delete tasks from an IRIS case

#### iris_add_assets.py
* Add assets to IRIS from a CSV file

#### iris_get_from_ts.py
* Get Timeline events from TimeSketch

#### iris_add_iocs_misp.py
* Add IOCs from MISP to IRIS

#### iris_add_evidence.py
* Add evidence to IRIS

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
