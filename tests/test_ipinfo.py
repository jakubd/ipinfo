from ipinfo import IpInfo

def test_ipinfo_init():
    ii = IpInfo()
    assert ii

def test_ipinfo_is_ip_valid():
    ii = IpInfo()
    assert ii.is_ip_valid(1)
    assert ii.is_ip_valid("127.0.0.1")
    assert ii.is_ip_valid("8.8.8.8")
    assert not ii.is_ip_valid("s")

def test_ipinfo_get_meta():
    ii = IpInfo()
    meta_str = ii.get_meta()
    assert len(meta_str) == 55
    assert meta_str.startswith("GeoLite2-ASN_")

def test_ipinfo_is_ip_private():
    ii = IpInfo()
    assert ii.is_ip_private("127.0.0.1")
    assert not ii.is_ip_private("8.8.8.8")
    assert not ii.is_ip_private("asfdasfd")

def test_ip_to_country_code():
    ii = IpInfo()
    assert ii.ip_to_country_code("8.8.8.8") == "US"
    assert ii.ip_to_country_code("2.57.168.0") == "CA"

def test_ip_to_country_name():
    ii = IpInfo()
    assert ii.ip_to_country_name("8.8.8.8") == "United States"
    assert ii.ip_to_country_name("2.57.168.0") == "Canada"

def test_domain_to_ip():
    ii = IpInfo()
    g_ip = ii.domain_to_ip("dns.google")
    assert g_ip == "8.8.8.8" or g_ip == "8.8.4.4"
    cf_ip = ii.domain_to_ip("one.one.one.one")
    assert cf_ip == "1.1.1.1" or cf_ip == "1.0.0.1"
#
def test_domain_to_ip_full():
    ii = IpInfo()
    cf = ii.domain_to_ip_full("one.one.one.one")
    assert len(cf) == 2
    for cf_ip in cf:
        assert cf_ip == "1.1.1.1" or cf_ip == "1.0.0.1"

def test_ip_to_asn_num():
    ii = IpInfo()
    assert ii.ip_to_asn_num("8.8.8.8") == 15169
    assert ii.ip_to_asn_num("8.8.df8.8") == -1

def test_ip_to_asn_name():
    ii = IpInfo()
    assert ii.ip_to_asn_name("8.8.8.8") == "Google LLC"
    assert ii.ip_to_asn_name("8dfs.8.8.8") == ""

def test_ip_to_reverse_dns():
    ii = IpInfo()
    assert ii.ip_to_reverse_dns("1.1.1.1") == "one.one.one.one"
    assert ii.ip_to_reverse_dns("8.8.8.8") == "dns.google"

def test_input_to_ip():
    ii = IpInfo()
    g_ip = ii.input_to_ip("dns.google")
    assert g_ip == "8.8.8.8" or g_ip == "8.8.4.4"
#
def test_input_is_what():
    ii = IpInfo()
    assert ii.input_is_what("8.8.8.8") == "ip"
    assert ii.input_is_what(" 8.8.8.8 ") == "ip"
    assert ii.input_is_what("dns.google") == "domain"
    assert ii.input_is_what("asdfasdf") == "unknown"

def test_ip_details():
    ii = IpInfo()
    deets = ii.ip_details("8.8.8.8")
    assert deets["ip"] == "8.8.8.8"
    assert deets["input_type"] == "ip"
    assert deets["reverse_dns"] == "dns.google"
    assert deets["maxmind_asn_name"] == "Google LLC"
    assert deets["maxmind_country_code"] == "US"
    assert deets["maxmind_country_name"] == "United States"

def test_ip_details_list():
    ii = IpInfo()
    testlist = [
        "8.8.8.8",
        "1.1.1.1"
    ]

    deetlist = ii.ip_details_list(testlist)
    assert len(deetlist) == 2

    assert deetlist[0]["ip"] == "8.8.8.8"
    assert deetlist[0]["input_type"] == "ip"
    assert deetlist[0]["reverse_dns"] == "dns.google"
    assert deetlist[0]["maxmind_asn_name"] == "Google LLC"
    assert deetlist[0]["maxmind_country_code"] == "US"
    assert deetlist[0]["maxmind_country_name"] == "United States"

    assert deetlist[1]["ip"] == "1.1.1.1"
    assert deetlist[1]["input_type"] == "ip"
    assert deetlist[1]["reverse_dns"] == "one.one.one.one"
    assert deetlist[1]["maxmind_asn_name"] == "Cloudflare, Inc."
    assert deetlist[1]["maxmind_country_code"] == "AU"
    assert deetlist[1]["maxmind_country_name"] == "Australia"

    print("done")

