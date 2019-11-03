import sys
import ipinfo

ii = ipinfo.IpInfo()

for this_std_in_line in sys.stdin:
    this_std_in_line = this_std_in_line.rstrip("\n")
    details = ii.ip_details(this_std_in_line)

    full = [details["given_input"],
            details["ip"], details["domain"], details["reverse_dns"],
            details["maxmind_asn_name"], details["maxmind_asn_num"],
            details["maxmind_country_code"], details["maxmind_country_name"]]

    compact = [details["ip"], details["maxmind_asn_name"], details["maxmind_asn_num"],
               details["maxmind_country_code"]]

    print(full)
    print(compact)

def stub():
    pass
