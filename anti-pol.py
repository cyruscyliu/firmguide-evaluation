#!/usr/bin/python
import json
import argparse

from prettytable import PrettyTable
from pol import compare


def anti_pol(args):
    with open(args.file) as f:
        statistics = json.load(f)

    table = PrettyTable()
    table.field_names = ['K1', 'K2', 'GROUP', 'CPUD', 'INTCD', 'TIMERD', 'SERIALD', 'SUMD']

    for k1, v1 in statistics.items():
        for k2_1, v2_1 in v1.items():
            for k2_2, v2_2 in v1.items():
                if k2_1 == k2_2:
                    continue
                for g1, inst1 in enumerate(v2_1):
                    for g2, inst2 in enumerate(v2_2):
                        d1, d2, d3, d4 = compare(inst1, inst2)
                        table.add_row([k1, k2_1, '{}-{}-{}-{}'.format(k2_1, k2_2, g1, g2),
                                    d1, d2, d3, d4, d1 + d2 + d3 + d4])

    if args.json:
        print(table.get_json_string())
    elif args.csv:
        print(table.get_csv_string())
    else:
        print(table.get_string())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--file', required=True,
                        help='Horizontal/Vertical statistics input.')
    parser.add_argument('-j', '--json',
                        help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv',
                        help='Generate CSV data.', action='store_true', default=False)
    args = parser.parse_args()
    anti_pol(args)
