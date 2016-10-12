from sys import exit
from getpass import getpass
from argparse import ArgumentParser
from pprint import pprint as pp
from veeamclient import VeeamSession, VeeamReports

parser = ArgumentParser()

parser.add_argument(
    '--username',
    required=True
)

parser.add_argument(
    '--hostname',
    default='localhost',
    help='Veeam Enterprise Manager hostname'
)

parser.add_argument(
    '--password'
)

parser.add_argument(
    '--read-password',
    action='store_true',
    default=False,
    help='Read password from stdin.'
)

parser.add_argument(
    '--use-ssl',
    action='store_true',
    default=False
)

parser.add_argument(
    '--verify-ssl',
    action='store_true',
    default=False
)

args = parser.parse_args()

if args.read_password:
    password = getpass('Password: ')
else:
    if not args.password:
        print('Must provide password on command line or from stdin')
        exit(1)
    password = args.password

v = VeeamSession(
    hostname=args.hostname,
    username=args.username,
    password=password,
    use_tls=args.use_ssl,
    verify_tls=args.verify_ssl
)
