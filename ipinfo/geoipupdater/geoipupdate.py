# TODO: class that will help keep geoip databases up-to-date

from ipinfo.configreader import ConfigReader
import os

class GeoIpUpdater:

    MAXMIND_CTRY_URL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
    MAXMIND_ASN_URL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz"

    MAXMIND_COUNTRY_FN = "GeoLite2-Country.mmdb"
    MAXMIND_ASN_FN = "GeoLite2-ASN.mmdb"

    def __init__(self):
        self.cfg = ConfigReader()
        self.geoip_dir = self.cfg.get_geoip_dir()

    def check_if_have_complete_db(self):
        if self.check_if_file_exists(os.path.join(self.geoip_dir, self.MAXMIND_COUNTRY_FN)) and \
                self.check_if_file_exists(os.path.join(self.geoip_dir, self.MAXMIND_ASN_FN)):
            return True
        return False

    @staticmethod
    def check_if_file_exists(given_full_path):
        if not os.path.exists(given_full_path) or not os.path.isfile(given_full_path):
            return False

        return True
