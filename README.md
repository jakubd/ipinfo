[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Build Status](https://travis-ci.org/jakubd/ipinfo.svg?branch=master)](https://travis-ci.org/jakubd/ipinfo)

# ipinfo

A light wrapper for performing Maxmind GeoIP lookups from local databases that will retreive country
and ASN information in the CLI. Takes care of keeping the databases up-to-date.

# Prerequisites

Tested on Debian 9/10 on: 

* Python 2.7.17
* Python 3.6.9
* Python 3.7.5
* PYthon 3.8.0

For those system you only need to have pip installed such as via `python3-pip` package in order
to install. 

# Installation

Simply run:

```
./install.sh
```

and it will install into your current virtualenv or python environment. 

You will also need to download the MaxMind GeoLite databases first with `ipinfoupdate`:

```bash
$ ipinfodbupdate 
updating geoip databases to directory: ~/.config/ipinfo/
done!
```

By default it stores the Maxmind database files in your home config folder: `~/.config/ipinfo`.  
You can change this by editing `~/.config/ipinfo/ipinfo.yml`.  For example if you want it to work system-wide 
or be updated with `geoipupdate` instead you can change this value to `/var/lib/GeoIP`

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
