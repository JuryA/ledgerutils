#!/usr/bin/env python
# coding=utf-8

import sys
import os
import configparser
import argparse
import dateutil.parser

from modules import alelo, conectcar, fuel, itau, nubank, qif
from ledger import load_list_csv

def convert(account_type, args):
    input_file = None

    # Command line has priority over config file
    if args.input_file:
        input_file = args.input_file
    elif conf and 'input_file' in conf:
        input_file = open(conf['input_file'], "r")
    else:
        print "Input file needed"

    if input_file:
        MODULES[account_type].read_file(input_file)

def online(account_type, args):
    if account_type == "alelo":
        card_number = None

        if len(args.info) == 1:
            card_number = args.info[0]
        elif conf and 'card_number' in conf:
            card_number = conf['card_number']

        if card_number:
            MODULES[account_type].online(card_number=card_number)
        else:
            print "Card number needed"

    else:
        username = None
        password = None

        if conf and 'username' in conf:
            username = conf['username']
        if conf and 'password' in conf:
            password = conf['password']

        if len(args.info) == 2:
            username = args.info[0]
            password = args.info[1]
        elif len(args.info) == 1:
            username = args.info[0]

        if username and password:
            MODULES[account_type].online(username, password)
        else:
            print "Missing username and/or password"

parser = argparse.ArgumentParser(
        description="Utilities to help with plaintext accounting.")
parser.add_argument("-d", type=str, metavar="DATE", dest="date",
        help="Start parsing from this date")

subparsers = parser.add_subparsers(help="Command to run")

parser_convert = subparsers.add_parser("convert", help="Convert file into ledger format")
parser_convert.add_argument("account", type=str, help="Format name")
parser_convert.add_argument("-i", type=argparse.FileType("r"), default=None,
        dest="input_file", metavar="INPUT",
        help="Input file used by the parser")
parser_convert.add_argument("-o", type=argparse.FileType("r"), default=None,
        dest="output_file", metavar="OUTPUT",
        help="Output file to write new entries")
parser_convert.set_defaults(func=convert)

parser_online = subparsers.add_parser("online", help="Get information online")
parser_online.add_argument("account", type=str, help="Format name")
parser_online.add_argument("info", type=str, nargs='*', help="Infos to access")
parser_online.add_argument("-o", type=argparse.FileType("r"), default=None,
        dest="output_file", metavar="OUTPUT",
        help="Output file to write new entries")
parser_online.set_defaults(func=online)

args = parser.parse_args()

CONFIG = configparser.ConfigParser()
conf = None
from_date = None
output_file = None
account_type = args.account

load_list_csv()

if os.path.isfile('ledgerutils.conf'):
    CONFIG.read('ledgerutils.conf')

if args.account in CONFIG.sections():
    conf = CONFIG[args.account]

if args.date:
    from_date = dateutil.parser.parse(args.date).timetuple()

if args.output_file:
    output_file = args.output_file
elif conf and 'output_file' in conf:
    output_file = open(conf['output_file'], "r")

if conf and "account_type" in conf:
    account_type = conf["account_type"]

MODULES = {
    'alelo': alelo.Alelo(conf, output_file=output_file, from_date=from_date),
    'conectcar': conectcar.ConectCar(conf, output_file=output_file, from_date=from_date),
    'fuel': fuel.Fuel(conf, output_file=output_file, from_date=from_date),
    'itau': itau.Itau(conf, output_file=output_file, from_date=from_date),
    'nubank': nubank.Nubank(conf, output_file=output_file, from_date=from_date),
    'qif': qif.QIF(conf, output_file=output_file, from_date=from_date)
}

args.func(account_type, args)
