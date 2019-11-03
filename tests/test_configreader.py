from ipinfo.configreader import ConfigReader
import pytest

def test_init():
    cfg = ConfigReader()
    assert cfg

def test_check_major_section():
    cfg = ConfigReader()
    cfg.check_major_section("directories")

    with pytest.raises(ValueError):
        cfg.check_major_section("Asdfasd")

def test_check_key():
    cfg = ConfigReader()
    cfg.check_key("directories", "geoip_dir")

    with pytest.raises(ValueError):
        cfg.check_key("directories", "asdf")

def test_get_db_info():
    cfg = ConfigReader()
    # TODO: test after updater done
    # dbinfo = cfg.get_db_info()
    # assert dbinfo

def test_get_geoip_dir():
    cfg = ConfigReader()
    geoip_dir = cfg.get_geoip_dir()
    assert geoip_dir == "/var/lib/GeoIP"