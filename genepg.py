"""
Generate XML TV
"""

import sys
import argparse
import XmlTvGen

def main(argv):
    parser = argparse.ArgumentParser(description='XML TV EPG generator with multiple languages support')
    parser.add_argument('-s', '--start', nargs=1, help='EPG start date')
    parser.add_argument('-e', '--end', nargs=1, help='EPG end date')
    parser.add_argument('-l', '--langs', nargs='+', help='csv list of languages')
    #args = parser.parse_args('2014-12-12 2014-12-14 en,fa'.split())
    args = parser.parse_args()
    #print args

if __name__ == '__main__':
    main(sys.argv)