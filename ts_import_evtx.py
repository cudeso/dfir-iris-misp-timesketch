from timesketch_api_client import config
from timesketch_import_client import importer
from lxml import etree
import Evtx.Evtx as evtx
import Evtx.Views as e_views
from pprint import pprint


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Import EVTX file into TimeSketch")
    parser.add_argument("sketch_id", type=int, help="TimeSketch ID")
    parser.add_argument("evtx", type=str, help="Path to the Windows EVTX event log file")
    args = parser.parse_args()

    ts = config.get_client()
    my_sketch = ts.get_sketch(args.sketch_id)

    ts_records = []
    with evtx.Evtx(args.evtx) as log:
        record_count_evtx = 0
        for record in log.records():
            #pprint(record.xml())
            ts_record = {}
            node = record.lxml()
            for tag in node.iter():
                if not len(tag):
                    key = tag.tag.split("event}")[1]
                    value = tag.text
                    if key == "Data":
                        for data in tag.iter():
                            data_tag = data.xpath("@Name")[0]
                            data_value = data.text
                            ts_record[data_tag] = data_value
                    else:
                        if key == "TimeCreated":
                            ts_record[key] = tag.xpath("@SystemTime")[0]
                        elif key == "Execution":
                            ts_record[key] = tag.xpath("@ProcessID")[0]
                        elif key == "Security":
                            ts_record[key] = tag.xpath("@UserID")[0]
                        else:
                            ts_record[key] = tag.text
            ts_record["parser"] = "ts_import_evtx"
            ts_record["event_identifier"] = ts_record["EventID"]        # for tagging
            ts_records.append(ts_record)
            record_count_evtx += 1
    
    with importer.ImportStreamer() as streamer:
        streamer.set_sketch(my_sketch)
        streamer.set_timestamp_description('Windows EVTX file')
        streamer.set_timeline_name(args.evtx)
        streamer.set_message_format_string('{Computer:s} EvenID:{EventID:s} {SubjectUserName:s} {ProcessName:s}')
        record_count_ts = 0
        for record in ts_records:
            if 'ProcessName' not in record or record["ProcessName"] == None:
                record["ProcessName"] = ""
            if 'SubjectUserName' not in record or record["SubjectUserName"] == None:
                record["SubjectUserName"] = ""
            streamer.add_dict(
                record
            )
            record_count_ts += 1

    print("{} records from EVTX imported into {} records in TimeSketch".format(record_count_evtx, record_count_ts))


if __name__ == "__main__":
    main()
