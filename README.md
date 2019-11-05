# ipinfo

A light wrapper for performing Maxmind GeoIP lookups from local databases that will retreive country
and ASN information in the CLI. Takes care of keeping the databases up-to-date but can also work
with `geoipupdate` and manually selected databases.

# Installation

Simply run:

```
./install.sh
```

and it will install into your current virtualenv. You will need to update the MaxMind database first with

```bash
$ ipinfodbupdate 
updating geoip databases to directory: /var/lib/GeoIP
done!
```

It uses the directory `/var/lib/GeoIP` by default because the `geoipupdate` app also uses it.  You can change it
by editing `~/.config/ipinfo/ipinfo.yml`.

# Supported Platform

Tested on Linux Debian on both Python 2.7 and 3.7.

# Usage

Can pipe input to ipinfo, for quick minimal info.
 
```
$ echo "8.8.8.8" | ipinfo
8.8.8.8,15169,Google LLC,US
```

Can select full field output with `-ff`, this will return a full cite-able record of the database used to perform the 
lookup.  Can also show headers with `-sh`

```
 $ echo "8.8.8.8" | ipinfo -ff -sh
input,input_type,ip,domain,rdns,asn_name,asn_num,cc,country,db_used
8.8.8.8,ip,8.8.8.8,,dns.google,Google LLC,15169,US,United States,GeoLite2-ASN_1572298980-and-GeoLite2-Country_1572298980
```

Also can support a table output with output table `-ot`:

```
$ echo "8.8.8.8" | ipinfo -sh -ot    
| ip      |   asn_num | asn_name   | cc   |
|---------|-----------|------------|------|
| 8.8.8.8 |     15169 | Google LLC | US   |
```

Can also go through txt file of ips with `-il`

```
$ ipinfo -il ips.txt -sh
ip,asn_num,asn_name,cc
8.8.8.8,15169,Google LLC,US
8.8.4.4,15169,Google LLC,US
1.1.1.1,13335,"Cloudflare, Inc.",AU
```
