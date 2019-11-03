# TODO: class that will help keep geoip databases up-to-date

from ipinfo.configreader import ConfigReader
import os
import requests
import tarfile

class GeoIpUpdater:

    MAXMIND_COUNTRY_URL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
    MAXMIND_ASN_URL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz"

    MAXMIND_COUNTRY_FN = "GeoLite2-Country.mmdb"
    MAXMIND_ASN_FN = "GeoLite2-ASN.mmdb"

    def __init__(self):
        self.cfg = ConfigReader()
        self.geoip_dir = self.cfg.get_geoip_dir()

    def get_country_db_fn(self):
        return os.path.join(self.geoip_dir, self.MAXMIND_COUNTRY_FN)

    def get_asn_db_fn(self):
        return os.path.join(self.geoip_dir, self.MAXMIND_ASN_FN)  

    def untar_mmdb(self, given_fn):
        tar = tarfile.open(given_fn, "r:gz")
        members = [m.name for m in tar.getmembers() if m.name.endswith(".mmdb")]
        if len(members) == 0:
            raise FileNotFoundError
        fn = members[0]

        if given_fn.find("ASN") > 0:
            unzipped_fn = self.MAXMIND_ASN_FN
        elif given_fn.find("Country") > 0:
            unzipped_fn = self.MAXMIND_COUNTRY_FN
        else:
            raise ValueError

        f = open(os.path.join(self.geoip_dir, unzipped_fn), "wb")
        for buf in tar.extractfile(fn):
            f.write(buf)

        f.close()
        tar.close()

    @staticmethod
    def download_file(given_url, dest_dir=""):
        if dest_dir == "":
            dest_dir = os.path.dirname(os.path.realpath(__file__))

        if given_url.find('/'):
            dest_fn = given_url.rsplit('/', 1)[1]
        else:
            dest_fn = "unknown_file"
        r = requests.get(given_url)
        open(os.path.join(dest_dir, dest_fn), 'wb').write(r.content)

    def update_detailed(self, given_db_fn, given_db_url, given_zipped_fn):
        if not self.check_if_file_exists(os.path.join(self.geoip_dir, given_db_fn)):
            self.download_file(given_db_url, dest_dir=self.geoip_dir)
            zipped_fn_country = os.path.join(self.geoip_dir, given_zipped_fn)
            self.untar_mmdb(zipped_fn_country)
            os.remove(zipped_fn_country)

    def update(self):
        self.update_detailed(self.MAXMIND_COUNTRY_FN, self.MAXMIND_COUNTRY_URL, "GeoLite2-Country.tar.gz")
        self.update_detailed(self.MAXMIND_ASN_FN, self.MAXMIND_ASN_URL, "GeoLite2-ASN.tar.gz")

    def force_update(self):
        if os.path.isfile(self.get_asn_db_fn()):
            os.remove(self.get_asn_db_fn())

        if os.path.isfile(self.get_country_db_fn()):
            os.remove(self.get_country_db_fn())

        self.update()

    def check_if_have_complete_db(self):
        if self.check_if_file_exists(self.get_country_db_fn()) and \
                self.check_if_file_exists(self.get_asn_db_fn()):
            return True
        return False

    @staticmethod
    def check_if_file_exists(given_full_path):
        if not os.path.exists(given_full_path) or not os.path.isfile(given_full_path):
            return False

        return True
