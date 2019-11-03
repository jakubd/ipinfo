import os
import yaml
import logging

class ConfigReader:

    cfg = None

    cfg_dirname = ""

    DEF_CFG = """
directories:
    geoip_dir: /var/lib/GeoIP    
"""

    def __init__(self, given_explicit_config_filename=None):
        if not given_explicit_config_filename:

            self.cfg_dirname = os.path.join(os.path.expanduser("~"), ".config", "ipinfo")
            if not os.path.exists(self.cfg_dirname):
                os.makedirs(self.cfg_dirname)

            cfg_file_path = os.path.join(self.cfg_dirname, "ipinfo.yml")

            if not os.path.exists(cfg_file_path):
                with open(cfg_file_path, "a") as f:
                    f.write(self.DEF_CFG)

            self.config_fn = os.path.join(self.cfg_dirname, "ipinfo.yml")

        else:
            self.config_fn = given_explicit_config_filename

        try:
            f = open(self.config_fn, 'r')
        except IOError:
            logging.error("No config found at path:", self.config_fn)
            raise

        try:
            self.cfg = yaml.load(f, Loader=yaml.BaseLoader)
        except yaml.YAMLError:
            logging.error("Error parsing config file at:", self.config_fn)
            raise

        f.close()

        self.check_major_section("directories")
        self.check_key("directories", "geoip_dir")

    def check_major_section(self, section):
        if section not in self.cfg:
            logging.error("Configfile is invalid at:", self.config_fn)
            if section:
                logging.error("Missing section", section)
                raise ValueError

    def check_key(self, section, key):
        if key not in self.cfg[section]:
            logging.error("Missing key:", key,"in section:", section, "in config file:", self.config_fn)
            raise ValueError

    def get_geoip_dir(self):
        return self.cfg["directories"]["geoip_dir"]
