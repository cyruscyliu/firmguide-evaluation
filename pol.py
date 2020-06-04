#!/usr/bin/python
import os
import argparse

from prettytable import PrettyTable


BUILD = '/mnt/iscsi/autobots-buildenv-trail'


def pol(args):
    # table = PrettyTable()

    with open('lq.batch') as f:
        for line in f:
            if line.startswith('SUCC') or line.startswith('FAIL'):
                _, _, key = line.strip().strip(',').split()
                rv = key.split('-')[1]
                d = os.path.join(BUILD, '{}-autobots-{}'.format(rv, key))
                if not os.path.exists(d):
                    print('>>>> ERROR <<<< {} doesn\'t exist'.format(d))
                if line.startswith('FAIL'):
                    print('>>>> ERROR <<<< {} fails'.format(d))
    # if args.json:
        # print(table.get_json_string(sortby='count', reversesort=True))
    # elif args.csv:
        # print(table.get_csv_string(sortby='count', reversesort=True))
    # else:
        # print(table.get_string(sortby='count', reversesort=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)

    args = parser.parse_args()
    pol(args)
