#!/usr/bin/python
import json
import argparse

from prettytable import PrettyTable


def flatten_inst(inst):
    r = []
    for ins in inst:
        r.extend(ins)
    return r


def really_compare(inst1, inst2):
    flatten1 = set(flatten_inst(inst1))
    flatten2 = set(flatten_inst(inst2))
    diff = flatten1.difference(flatten2)
    return len(diff)


def compare(inst1, inst2):
    d1 = really_compare(inst1['cpus'], inst2['cpus'])
    d2 = really_compare(inst1['intcs'], inst2['intcs'])
    d3 = really_compare(inst1['timers'], inst2['timers'])
    d4 = really_compare(inst1['serials'], inst2['serials'])
    return d1, d2, d3, d4


def pol(args):
    with open(args.file) as f:
        statistics = json.load(f)

    table = PrettyTable()
    table.field_names = ['K1', 'K2', 'GROUP', 'CPUD', 'INTCD', 'TIMERD', 'SERIALD', 'SUMD']

    for k1, v1 in statistics.items():
        for k2, v2 in v1.items():
            for g1, inst1 in enumerate(v2):
                for g2, inst2 in enumerate(v2):
                    d1, d2, d3, d4 = compare(inst1, inst2)
                    table.add_row([k1, k2, '{}-{}'.format(g1, g2),
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
    pol(args)
