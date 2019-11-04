import sys
import ipinfo
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-of', '--output-full', action='store_true', default=False, help="shows all fields in output")
parser.add_argument('-oc', '--output-compact', action='store_true', default=True, help="shows minimal fields")
parser.add_argument('-oh', '--output-headers', action='store_true', default=False, help="shows header row")
parser.add_argument('-il', '--input-list', type=str, default=False, help="txt file of ips to be taken as input")
args = parser.parse_args()

ii = ipinfo.IpInfo()

show_headers = True

full_headers = ["input", "ip", "domain", "rdns", "asn_name", "asn_num", "cc", "country"]
def get_full(d):
    return [d["given_input"], d["ip"], d["domain"], d["reverse_dns"], d["maxmind_asn_name"],
            d["maxmind_asn_num"], d["maxmind_country_code"], d["maxmind_country_name"]]


compact_headers = ["ip", "asn_name", "asn_num", "cc"]
def get_compact(d):
    return [d["ip"], d["maxmind_asn_name"], d["maxmind_asn_num"], d["maxmind_country_code"]]


first_row = True
f = None
output_target = sys.stdin

if args.input_list:
    try:
        f = open(args.input_list, "r")
    except FileNotFoundError:
        logging.error("Can't open file for input: %s" % args.input_list)
    output_target = f

for this_std_in_line in output_target:
    this_std_in_line = this_std_in_line.rstrip("\n")
    details = ii.ip_details(this_std_in_line)

    if args.output_full:
        if first_row and args.output_headers:
            first_row = False
            print(full_headers)
        full = get_full(details)
        print(full)
    elif args.output_compact:
        if first_row and args.output_headers:
            first_row = False
            print(compact_headers)
        compact = get_compact(details)
        print(compact)

if f is not None:
    f.close()

def stub():
    pass
