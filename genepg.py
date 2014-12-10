# coding=utf-8
"""
Generate XML TV
"""

import sys
import argparse
import datetime as dt
from XmlTvGen import XmlTvGen

channels = [('Channel1', ['Channel1', 'Ch1'], 'movie')]


def main():
    now = dt.datetime.now()
    parser = argparse.ArgumentParser(prog='genepg.py', description='XML TV EPG generator with multiple languages support',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=200,
                                                                                         width=200))
    parser.add_argument('-s', '--start', nargs=1, default=now.strftime('%Y-%m-%d'),
                        help='EPG start date (default: today)')
    parser.add_argument('-e', '--end', nargs=1, default=(now + dt.timedelta(days=1)).strftime('%Y-%m-%d'),
                        help='EPG end date (default: today + 1 day)')
    parser.add_argument('-l', '--langs', nargs='+', default=['en'], help='List of languages (default: en)')
    parser.add_argument('-t', '--tz', nargs=1, default='+0000', help='Timezone offset (default: +0100)')
    parser.add_argument('-o', '--output', nargs=1, default='xmltv.tar.gz', help='Output tar.gz archive file, \
                                                                                 (default: xmltv.tar.gz)')

    # Print help message if no arguments are passed to the program, otherwise proceed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    #print args

    #xmltv = XmlTvGen(args.langs, args.start, args.end, channels, 'data/movies.csv', timezone=args.tz)
    #print xmltv

if __name__ == '__main__':
    main()