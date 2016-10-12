#!/usr/bin/env python3
# This can be done even with Enterprise license, a lot of other
# features require Enterprise Plus license.

from sys import exit
from getpass import getpass
from argparse import ArgumentParser, FileType
try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser

from veeamclient import VeeamSession, VeeamReports

parser = ArgumentParser()

parser.add_argument(
    '--config', '-c',
    type=FileType('r'),
    required=True
)

args = parser.parse_args()

config = RawConfigParser()
config.readfp(args.config)

v = VeeamSession(
    hostname=config.get('veeam', 'hostname'),
    username=config.get('veeam', 'username'),
    password=config.get('veeam', 'password'),
    use_tls=config.getboolean('veeam', 'use_ssl'),
    verify_tls=config.getboolean('veeam', 'verify_ssl')
)

reports = VeeamReports(v)
statistics = reports.job_statistics
for stat in statistics:
    # Fugli hack to get rid of the namespace prefix in tag names, assuming
    # your namespace dict only has one namespaces defined.
    print('{job}: {status}'.format(
        job=stat.tag.replace(
            '{{{ns}}}'.format(
                ns=list(v.namespace.values())[0]
            ), ''),
        status=stat.text
    ))
