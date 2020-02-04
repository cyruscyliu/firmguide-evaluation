#!/usr/bin/python
import os
import sys
import json
from prettytable import PrettyTable


WORKING_DIR = '/root/build'

pt = PrettyTable(['uuid', 'unpacked', 'profiled', 'user_level'])

rows = {}
summary = {'unpacked': 0, 'profiled': 0, 'user_level': 0}

def stats(argv):
    for log in os.listdir('log'):
        if not log.endswith('log'):
            continue
        uuid = log.split('.')[0]
        if uuid == 'salamander':
            continue

        rows[uuid] = {}

        log_path = os.path.join('log', log)

        # 1. whether this firmware can be unpacked
        unpacked = True
        profiled = False
        successful = False

        with open(log_path) as f:
            for line in f:
                if line.find('cannot unpack this firmware of nonstandard format') != -1:
                    unpacked = False
                if line.find('migrate from') != -1:
                    board = line.strip().split(' - ')[6].strip().split()[2].split('/')[5]
                    profiled = board
                if line.find('have entered the user level') != -1:
                    successful = True
        rows[uuid]['unpacked'] = unpacked
        rows[uuid]['profiled'] = profiled
        rows[uuid]['user_level'] = successful
        if unpacked:
            summary['unpacked'] += 1
        if profiled:
            summary['profiled'] += 1
        if successful:
            summary['user_level'] += 1
            pt.add_row([uuid, rows[uuid]['unpacked'], rows[uuid]['profiled'], rows[uuid]['user_level']])
    pt.add_row([
        'sum',
        '{:.2f}% ({}/{})'.format(summary['unpacked']/len(rows)*100, summary['unpacked'], len(rows)),
        '{:.2f}% ({}/{})'.format(summary['profiled']/len(rows)*100, summary['profiled'], len(rows)),
        '{:.2f}% ({}/{})'.format(summary['user_level']/len(rows)*100, summary['user_level'], len(rows)),
    ])

    if len(argv) == 2 and argv[1] == '-j':
        print(pt.get_json_string())
    else:
        print(pt)

if __name__ == '__main__':
    stats(sys.argv)

