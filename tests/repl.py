from sys import exit
from getpass import getpass
from argparse import ArgumentParser, FileType
from pprint import pprint as pp
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
