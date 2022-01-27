from timesketch_api_client import config
from timesketch_import_client import importer
from pprint import pprint
from scapy.all import *
from scapy.layers import http
import sys
import datetime
import tzlocal


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Import a PCAP file into TimeSketch.")
    parser.add_argument("sketch_id", type=int, help="Sketch ID of TimeSketch")
    parser.add_argument("pcap", type=str, help="Path to the pcapfile")
    args = parser.parse_args()

    pcap_input = args.pcap
    my_sketch = args.sketch_id
    import_pcap(pcap_input, my_sketch)


def import_pcap(pcap_input, sketch_id):
    ts = config.get_client()
    my_sketch = ts.get_sketch(sketch_id)

    packets = rdpcap(pcap_input)
    ts_packets = []
    
    for packet in packets:
        if packet.haslayer(IP):
            # Set defaults
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            ts_temp_record = { "parser": "ts_import_pcap", "src_ip": src_ip, "dst_ip": dst_ip, "src_port": 0, "dst_port": 0, "proto": packet[IP].proto, "flags": str(packet[IP].flags), "version":packet[IP].version, "ttl": packet[IP].ttl }

            try:
                timestamp = datetime.datetime.utcfromtimestamp(packet.time).strftime("%Y-%m-%d %H:%M:%S.%f%z")
                ts_temp_record["timestamp"] = timestamp
            except:
                continue
            protocol = packet[IP].proto
            src_port = dst_port = icmp_type = icmp_code =  0
            #http_method = http_host = http_uri = dns_query = http_user_agent = tcp_long_flags = tcp_short_flags = rawload = http_url = ""
            tcp_long_flags = tcp_short_flags = ""
            tcp_flags = { 'F': 'FIN',    'S': 'SYN',    'R': 'RST',    'P': 'PSH',    'A': 'ACK',    'U': 'URG',    'E': 'ECE',    'C': 'CWR' }

            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                tcp_short_flags = str(packet[TCP].flags)
                for x in tcp_short_flags:
                    if len(tcp_long_flags) > 0:
                        tcp_long_flags = "{} {}".format(tcp_long_flags, tcp_flags[x])
                    else:
                        tcp_long_flags = "{}".format(tcp_flags[x])
                ts_temp_record["src_port"] = src_port
                ts_temp_record["dst_port"] = dst_port
                ts_temp_record["tcp_short_flags"] = tcp_short_flags
                ts_temp_record["tcp_long_flags"] = tcp_long_flags
                
            elif packet.haslayer(UDP):
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                ts_temp_record["src_port"] = src_port
                ts_temp_record["dst_port"] = dst_port
            elif packet.haslayer(ICMP):
                #icmp_type = packet[ICMP].type
                #icmp_code = packet[ICMP].code
                ts_temp_record["icmp_type"] = packet[ICMP].type
                ts_temp_record["icmp_code"] = packet[ICMP].code

            if packet.haslayer(http.HTTPRequest):
                http_layer = packet.getlayer(http.HTTPRequest)
                #pprint(http_layer.fields)
                if "Method" in http_layer.fields:
                    #http_method = http_layer.fields["Method"].decode()
                    ts_temp_record["http_method"] = http_layer.fields["Method"].decode()
                if "Host" in http_layer.fields:
                    #http_host = http_layer.fields["Host"].decode()
                    ts_temp_record["http_host"] = http_layer.fields["Host"].decode()
                if "Path" in http_layer.fields:
                    #http_uri = http_layer.fields["Path"].decode()
                    ts_temp_record["http_uri"] = http_layer.fields["Path"].decode()
                if "User_Agent" in http_layer.fields:
                    #http_user_agent = http_layer.fields["User_Agent"].decode()
                    ts_temp_record["http_user_agent"] = http_layer.fields["User_Agent"].decode()
                if "http_host" in ts_temp_record and "http_uri" in ts_temp_record and len(ts_temp_record["http_host"]) > 0 and len(ts_temp_record["http_uri"]) > 0:
                    #http_url = "http://{}{}".format(ts_temp_record["http_host"], ts_temp_record["http_uri"])
                    ts_temp_record["url"] = "http://{}{}".format(ts_temp_record["http_host"], ts_temp_record["http_uri"])

            elif packet.haslayer(DNS) and packet.getlayer(DNS).opcode == 0:
                try:
                    query = packet.getlayer(DNS).qd.qname
                    #dns_query = query.decode('utf-8').rstrip('.').decode()
                    ts_temp_record["dns_query"] = query.decode('utf-8').rstrip('.').decode()
                    ts_temp_record["domain"] = query.decode('utf-8').rstrip('.').decode()        # Add this for the analyzers
                except:
                    continue
            
            if packet.haslayer(Raw):
                #rawload = str(packet.getlayer(Raw).load)
                ts_temp_record["rawload"] = str(packet.getlayer(Raw).load)
                

            #ts_packets.append({"timestamp": timestamp, "src_ip": src_ip, "dst_ip": dst_ip, "src_port": src_port, "dst_port": dst_port, "protocol": protocol, "icmp_type": icmp_type, "icmp_code": icmp_code, "http_method": http_method, "http_host": http_host, "http_uri": http_uri, "http_user_agent": http_user_agent, "dns_query": dns_query, "tcp_long_flags": tcp_long_flags, "tcp_short_flags": tcp_short_flags, "rawload": rawload, "http_url":http_url})
            ts_packets.append(ts_temp_record)

    with importer.ImportStreamer() as streamer:
      streamer.set_sketch(my_sketch)
      streamer.set_timestamp_description('Network Log')
      streamer.set_timeline_name(pcap_input)
      streamer.set_message_format_string(
              '{src_ip:s}:{src_port:d}->{dst_ip:s}:{dst_port:d}')
      
      for packet in ts_packets:
            streamer.add_dict(packet)


def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1


if __name__ == "__main__":
    main()
