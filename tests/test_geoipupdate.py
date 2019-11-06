from ipinfo.geoipupdater import GeoIpUpdater
import os

long_running = False

def test_init():
    gipu = GeoIpUpdater()
    assert gipu
    assert gipu.geoip_dir == os.path.join(os.path.expanduser("~"), ".config", "ipinfo")

def test_check_if_file_exists():
    gipu = GeoIpUpdater()
    assert gipu
    assert gipu.check_if_file_exists("/var/log/auth.log")
    assert not gipu.check_if_file_exists("/var/log/authasdfasdfasd.log")

def test_download_file():
    gipu = GeoIpUpdater()
    gipu.download_file("http://google.com/favicon.ico", "/tmp/")
    assert os.path.isfile("/tmp/favicon.ico")
    os.remove("/tmp/favicon.ico")

def test_get_x_db_fn():
    gipu = GeoIpUpdater()
    dbfn = gipu.get_country_db_fn()
    assert dbfn == os.path.join(os.path.expanduser("~"), ".config", "ipinfo", "GeoLite2-Country.mmdb")
    asnfn = gipu.get_asn_db_fn()
    assert asnfn == os.path.join(os.path.expanduser("~"), ".config", "ipinfo", "GeoLite2-ASN.mmdb")
    print("done")

def test_update():
    if long_running:
        gipu = GeoIpUpdater()
        gipu.force_update()
