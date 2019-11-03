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

# def test_input_to_ip():
#     ii = IpInfo()
#
# def test_input_is_what():
#     ii = IpInfo()
#
# def test_ip_details():
#     ii = IpInfo()
#     assert True
#
# def test_ip_details_list():
#     ii = IpInfo()
#     assert True
