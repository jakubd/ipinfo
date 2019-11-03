from ipinfo.geoipupdater import GeoIpUpdater
import os

def test_init():
    gipu = GeoIpUpdater()
    assert gipu
    assert gipu.geoip_dir == "/var/lib/GeoIP"

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

def test_update():
    gipu = GeoIpUpdater()
    # gipu.update()