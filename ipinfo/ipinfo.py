"""
This submodule is a wrapper for getting basic IP information (ip, asn, country etc)
and handling IPs and domains as input.
"""

import socket
from datetime import  datetime
from .configreader import ConfigReader
from .geoipupdater import GeoIpUpdater
import dns.resolver
import geoip2.database
import geoip2.errors
from IPy import IP

class IpInfo(object):
    """
    This class handles basic information about IPs such as domain to ip, ip to country code, ip to asn.
    """

    config = ConfigReader()

    # geoip stuff
    geoip_database_base_dir = config.get_geoip_dir()
    """directory you can find the .mmdb files from MaxMind"""

    country_db_filename = 'GeoLite2-Country.mmdb'
    """filename of the mmdb used for the country db"""
    asn_db_filename = 'GeoLite2-ASN.mmdb'
    """filename of the mmdb used for the asn db"""

    _geoip_country_reader = geoip2.database.Reader
    """geoip2 Reader object for the Country database"""
    _geoip_asn_reader = geoip2.database.Reader
    """geoip2 Reader object for the ASN database"""

    geoip_country_database_name = ""
    """the name of the database used for Country lookups"""
    geoip_asn_database_name = ""
    """the name of the database used for ASN lookups"""

    def __init__(self):
        """initializes an IPInfo object and points to correct databases."""

        # geoip stuff
        self.geo = GeoIpUpdater()

        self._geoip_country_reader = geoip2.database.Reader(self.geo.get_country_db_fn())
        self.geoip_country_database_name = self._geoip_country_reader.metadata().database_type \
                                           + '_' \
                                           + str(self._geoip_country_reader.metadata().build_epoch)

        self._geoip_asn_reader = geoip2.database.Reader(self.geo.get_asn_db_fn())
        self.geoip_asn_database_name = self._geoip_asn_reader.metadata().database_type \
                                           + '_' \
                                           + str(self._geoip_country_reader.metadata().build_epoch)

    @staticmethod
    def is_ip_valid(given_ip):
        """
        Checks if a given ip string is a valid ip address

        - :param given_ip: the ip you are checking
        - :return: True if ip otherwise false.
        """
        given_ip = str(given_ip)
        try:
            socket.inet_aton(given_ip)
            return True
        except socket.error:
            return False

    def is_ip_private(self, given_ip):
        """
        Checks if a given ip string is in a private subnet.  Returns
        false on invalid ip.

        - :param given_ip: the ip you are checking
        - :return: Boolean if ip is in private subnet.
        """
        if given_ip == "127.0.0.1":
            return True

        return self.is_ip_valid(given_ip) and (IP(given_ip).iptype() == "PRIVATE")

    def ip_to_country_code(self, given_ip):
        """
        Returns ISO country code for the given IP

        - :param given_ip: IP address as a string
        - :return: Two letter all caps Country code
        """
        fail_response = "ZZ"
        try:
            response = self._geoip_country_reader.country(given_ip)
            if response.country.iso_code:
                return response.country.iso_code
            else:
                return fail_response
        except geoip2.errors.AddressNotFoundError:
            return fail_response

    def ip_to_country_name(self, given_ip):
        """
        Returns the full country name for the given IP

        - :param given_ip: IP address as a string
        - :return: String of country name
        """
        try:
            response = self._geoip_country_reader.country(given_ip)
        except geoip2.errors.AddressNotFoundError:
            return ""
        return response.country.name

    def ip_to_asn_num(self, given_ip):
        """
        Will give you asn number as int for the ip.

        - :param given_ip: IP address as a string
        - :return: asn number or -1 in case of error.
        """
        try:
            asn_info = self._geoip_asn_reader.asn(given_ip)
            asn_num = asn_info.autonomous_system_number
        except (ValueError, geoip2.errors.AddressNotFoundError):
            asn_num = -1

        return asn_num

    def ip_to_asn_name(self, given_ip):
        """
        Converts an IP to its ASN name

        - :param given_ip: IP address as string
        - :return: the full ASN name or blank string in case of error.
        """
        try:
            asn_info = self._geoip_asn_reader.asn(given_ip)
            asn_name = asn_info.autonomous_system_organization
        except (ValueError, geoip2.errors.AddressNotFoundError):
            asn_name = ""

        return asn_name

    def ip_to_asn_name_and_num(self, given_ip):
        """
        Converts an IP to its ASN name and number

        - :param given_ip: IP address as string
        - :return: tuple with asn name (str), number (int)
        """
        asn_num = self.ip_to_asn_num(given_ip)
        asn_name = self.ip_to_asn_name(given_ip)
        return asn_name, asn_num

    def ip_to_reverse_dns(self, given_ip):
        """
        Will return the reverse DNS for a given IP
        or return a blank string.
        :param given_ip:  The IP address as a string.
        :return: Either blank string or domain as string.
        """
        unsuccessful = ""
        if not self.is_ip_valid(given_ip):
            return unsuccessful

        ptr_ready_ip = IP(given_ip).reverseNames()[0]
        try:
            answers = dns.resolver.query(ptr_ready_ip, "PTR")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.DNSException, dns.exception.Timeout):
            return unsuccessful

        if len(answers.response.answer) > 0:
            if len(answers.response.answer[0].items) > 0:
                return str(answers.response.answer[0].items[0]).rstrip(".")

        return unsuccessful

    def domain_to_ip(self, given_domain):
        """
        Resolves a domain and returns an ip.  Only returns a simple 1 address response.

        - :param given_domain: domain you want to resolve as a string
        - :return: ip as string or error message
        """
        try:
            answers = dns.resolver.query(given_domain, "A")
            is_answer_ip = False
            dns_response = None
            answer_idx = 0
            while not is_answer_ip:
                if  answer_idx > len(answers.response.answer):
                    return "NO_IP_REPLY"

                dns_response = str(answers.response.answer[answer_idx].items[0])
                if self.is_ip_valid(dns_response):
                    is_answer_ip = True
                answer_idx += 1
        except dns.resolver.NXDOMAIN:
            dns_response = "NXDOMAIN"
        except dns.resolver.NoAnswer:
            dns_response = "NoAnswer"
        except dns.resolver.NoNameservers:
            dns_response = "NoNameservers"

        return dns_response

    def ip_details(self, given_input):
        details = {"given_input": given_input, "input_type": self.input_is_what(given_input),
                   "date_collected": datetime.now().strftime("%Y/%m/%d %H:%m:%S"), "ip": "", "ip_sampled": "",
                   "domain": "", "reverse_dns": "", "maxmind_asn_num": -1, "maxmind_asn_name": "",
                   "maxmind_country_code": "", "maxmind_country_name": "", "maxmind_db_used": ""}

        if details["input_type"] == "ip":
            details["ip"] = given_input
            details["ip_sampled"] = given_input
        elif details["input_type"] == "domain":
            details["domain"] = given_input
            ip_results = self.domain_to_ip_full(given_input)
            details["ip"] = ip_results
            if len(ip_results.split(", ")) > 1:
                details["ip_sampled"] = ip_results.split(", ")[0]
            else:
                details["ip_sampled"] = ip_results
        else:
            return details

        details["maxmind_asn_name"] = self.ip_to_asn_name(details["ip_sampled"])
        details["maxmind_asn_num"] = self.ip_to_asn_num(details["ip_sampled"])
        details["maxmind_country_code"] = self.ip_to_country_code(details["ip_sampled"])
        details["maxmind_country_name"] = self.ip_to_country_name(details["ip_sampled"])
        details["maxmind_db_used"] = self.get_meta()
        details["reverse_dns"] = self.ip_to_reverse_dns(details["ip_sampled"])

        return details

    def ip_details_list(self, given_list):
        """
        Get basic geoip information for a list of IPs
        :param given_list: a list of IP as strings
        :return:  a list of python dicts of schema { ip, asn_num, asn_name, country_code }
        """
        results = []
        for this_ip in given_list:
            this_result = self.ip_details(this_ip)
            results.append(this_result)
        return results

    def input_is_what(self, given_input):
        """
        Tests if the given thing is an ip, domain or unknown
        :param given_input: Thing you are testing
        :return: either "domain" , "ip" or "unknown"
        """
        ip = ""

        given_input = str(given_input).lower().rstrip().lstrip()
        if given_input.startswith("http://") or given_input.startswith("https://"):
            given_input = given_input.replace("http://", "")
            given_input = given_input.replace("https://", "")

        if not self.is_ip_valid(given_input):
            maybe_ip_now = self.domain_to_ip(given_input)
            if self.is_ip_valid(maybe_ip_now):
                return "domain"
            else:
                return "unknown"
        else:
            return "ip"

    def input_to_ip(self, given_input):
        """
        Try to resolve the given input to a single IP if possible (useful in cases where input may be domain or ip)

        :param given_input: the given thing you want to check
        :return: returns an ip or blank
        """

        thing = self.input_is_what(given_input)
        if thing == "ip":
            return given_input
        elif thing == "domain":
            return self.domain_to_ip(given_input)
        else:
            return ""

    @staticmethod
    def domain_to_ip_full(given_domain):
        """
        Similar to domain_to_ip() function except will return multiple address as well.

        - :param given_domain: domain you want to resolve as a string
        - :return: ip as a list
        """
        ip_list = []

        try:
            answers = dns.resolver.query(given_domain, 'A')
            for this_answer in answers:
                ip_list.append(str(this_answer))
        except dns.resolver.NXDOMAIN:
            ip_list.append("NXDOMAIN")
        except dns.resolver.NoAnswer:
            ip_list.append("NoAnswer")

        return ip_list

    def domain_to_ip_full_str(self, given_domain):
        iplist = self.domain_to_ip_full_str(given_domain)
        return ", ".join(iplist)

    def get_meta(self):
        """
        :return: Return a one line report of the databases used currently for geoip lookups
        """
        asndb = self.geoip_asn_database_name.replace(" ", "-")
        countrydb = self.geoip_country_database_name.replace(" ", "-")
        return asndb + "-and-" + countrydb
