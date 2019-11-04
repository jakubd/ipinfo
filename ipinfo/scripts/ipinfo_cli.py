import sys
import ipinfo
import argparse
import logging
import csv
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('-ff', '--fields-full', action='store_true', default=False, help="shows all fields in output")
parser.add_argument('-fc', '--fields-compact', action='store_true', default=True, help="shows minimal fields")
###
parser.add_argument('-sh', '--show-headers', action='store_true', default=False, help="shows header row")
###
parser.add_argument('-oc', '--output-csv', action='store_true', default=True, help="shows comma seperated output")
parser.add_argument('-ot', '--output-table', action='store_true', default=False, help="show table output")
###
parser.add_argument('-il', '--input-list', type=str, default=False, help="txt file of ips to be taken as input")
args = parser.parse_args()

ii = ipinfo.IpInfo()

show_headers = True

full_headers = ["input", "input_type", "ip", "domain", "rdns", "asn_name", "asn_num", "cc", "country", "db_used"]
def get_full(d):
    return [d["given_input"], d["input_type"], d["ip"], d["domain"], d["reverse_dns"],
            d["maxmind_asn_name"], d["maxmind_asn_num"],
            d["maxmind_country_code"], d["maxmind_country_name"], d["maxmind_db_used"]]


compact_headers = ["ip", "asn_name", "asn_num", "cc"]
def get_compact(d):
    return [d["ip"], d["maxmind_asn_name"], d["maxmind_asn_num"], d["maxmind_country_code"]]


if args.output_table:
    args.output_csv = False

first_row = True
f = None
output_target = sys.stdin
csv_writer = csv.writer(sys.stdout)
tabulate_tbl = []

if args.input_list:
    try:
        f = open(args.input_list, "r")
    except FileNotFoundError:
        logging.error("Can't open file for input: %s" % args.input_list)
    output_target = f

for this_std_in_line in output_target:
    this_std_in_line = this_std_in_line.rstrip("\n")
    details = ii.ip_details(this_std_in_line)

    if args.fields_full:
        if first_row and args.show_headers:
            first_row = False

            if args.output_csv:
                csv_writer.writerow(full_headers)
        full = get_full(details)
        if args.output_csv:
            csv_writer.writerow(full)
        elif args.output_table:
            tabulate_tbl.append(full)

    elif args.fields_compact:
        if first_row and args.show_headers:
            first_row = False
            if args.output_csv:
                csv_writer.writerow(compact_headers)
            elif args.output_table:
                pass
        compact = get_compact(details)
        if args.output_csv:
            csv_writer.writerow(compact)
        elif args.output_table:
            tabulate_tbl.append(compact)

if args.output_table and args.fields_full:
    print(tabulate(tabulate_tbl, headers=full_headers, tablefmt="github"))
elif args.output_table and args.fields_compact:
    print(tabulate(tabulate_tbl, headers=compact_headers, tablefmt="github"))

if f is not None:
    f.close()

def stub():
    pass
