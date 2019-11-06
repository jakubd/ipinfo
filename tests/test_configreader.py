from ipinfo.configreader import ConfigReader
import pytest
import os

def test_init():
    cfg = ConfigReader()
    assert cfg

def test_init_fresh():
    os.remove(os.path.join(os.path.expanduser("~"), ".config", "ipinfo", "ipinfo.yml"))
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

def test_get_geoip_dir():
    cfg = ConfigReader()
    geoip_dir = cfg.get_geoip_dir()
    assert geoip_dir == os.path.join(os.path.expanduser("~"), ".config", "ipinfo")
