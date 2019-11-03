import sys
import ipinfo

ii = ipinfo.IpInfo()

view = "full"
show_headers = True

full_headers = ["input", "ip", "domain", "rdns", "asn_name", "asn_num", "cc", "country"]
def get_full(d):
    return [d["given_input"], d["ip"], d["domain"], d["reverse_dns"], d["maxmind_asn_name"],
            d["maxmind_asn_num"], d["maxmind_country_code"], d["maxmind_country_name"]]


compact_headers = ["ip","asn_name", "asn_num", "cc"]
def get_compact(d):
    return [d["ip"], d["maxmind_asn_name"], d["maxmind_asn_num"],d["maxmind_country_code"]]


first_row = True
output_target = sys.stdin

for this_std_in_line in output_target:
    this_std_in_line = this_std_in_line.rstrip("\n")
    details = ii.ip_details(this_std_in_line)

    if view == "full":
        if first_row and show_headers:
            first_row = False
            print(full_headers)
        full = get_full(details)
        print(full)
    elif view == "compact":
        if first_row and show_headers:
            first_row = False
            print(compact_headers)
        compact = get_compact(details)
        print(compact)

def stub():
    pass
