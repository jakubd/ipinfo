import os
import yaml

class ConfigReader:

    cfg = None
    cfg_fn = ""

    cfg_dirname = ""

    def __init__(self, explicit_config_filename=None):
        if not explicit_config_filename:
            self.config_fn = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', 'conf' + os.sep + "ipinfo.yml"))
        else:
            self.config_fn = explicit_config_filename

        self.cfg_dirname = os.path.join(os.path.dirname(__file__), '..', '..', 'conf')

        try:
            f = open(self.config_fn, 'r')
        except IOError:
            print("No config found at path:", self.config_fn)
            raise

        try:
            self.cfg = yaml.load(f)
        except yaml.YAMLError:
            print("Error parsing config file at:", self.config_fn)
            raise

        f.close()

        self.check_major_section("directories")
        self.check_key("directories", "geoip_dir")

    def check_major_section(self, section):
        if section not in self.cfg:
            print("Configfile is invalid at:", self.config_fn)
            if section:
                print("Missing section", section)
                raise ValueError

    def check_key(self, section, key):
        if key not in self.cfg[section]:
            print("Missing key:", key,"in section:", section, "in config file:", self.config_fn)
            raise ValueError

    def get_db_info(self):
        return self.cfg["database"]

    def get_geoip_dir(self):
        return self.cfg["directories"]["geoip_dir"]
