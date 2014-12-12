# coding=utf-8
"""
Generate XML TV
"""

import sys
import argparse
from XmlTvGenerator.XmlTvGen     import XmlTvGen


channels = [('Channel1', ['Channel1', 'Ch1'], 'movie'),
            ('Channel2', ['Channel2', 'Ch2'], 'movie')]


def main():
    parser = argparse.ArgumentParser(prog='genepg.py', description='XML TV EPG generator with multiple languages support',
                                     epilog='Example usage: %(prog)s -a -l en fa -t +0330 -o xmltv.xml 2014-12-10 2014-12-12',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=200,
                                                                                         width=200))
    parser.add_argument('-i', '--images', action='store_true', default=False, help='Add image information to the EPG source')
    parser.add_argument('-a', '--archive', action='store_true', default=False, help='Archive the epg data in gziped tarbal')
    parser.add_argument('-l', '--langs', nargs='+', default=['en'], help='List of languages (default: en)')
    parser.add_argument('-t', '--tz', nargs='?', default='+0000', type=str, help='Timezone offset (default: +0000)')
    parser.add_argument('-o', '--output', nargs='?', default='xmltv.xml', type=str,
                        help='Output XML file (default: xmltv.xml)')
    parser.add_argument('START_DATE', type=str, help='EPG start date (format: YEAR-MONTH-DAY)')
    parser.add_argument('END_DATE', type=str, help='EPG end date (format: YEAR-MONTH-DAY)')

    # Print help message if no arguments are passed to the program, otherwise proceed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    #print args

    xmltv = XmlTvGen(args.langs, args.START_DATE, args.END_DATE, channels, 'data/movies.csv', timezone=args.tz, images=args.images)
    xmltv.write_epg_to_file(args.output, pretty=True, archive=args.archive)
    #print xmltv

if __name__ == '__main__':
    main()