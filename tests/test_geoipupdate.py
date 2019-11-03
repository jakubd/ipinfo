from ipinfo.geoipupdater import GeoIpUpdater

def test_init():
    gipu = GeoIpUpdater()
    assert gipu
    assert gipu.geoip_dir == "/var/lib/GeoIP"

def test_check_if_file_exists():
    gipu = GeoIpUpdater()
    assert gipu
    assert gipu.check_if_file_exists("/var/log/auth.log")
    assert not gipu.check_if_file_exists("/var/log/authasdfasdfasd.log")