#!/usr/bin/python
import os
from prettytable import PrettyTable


WORKING_DIR = '/root/build'

pt = PrettyTable(['uuid', 'unpacked', 'profiled'])

rows = {}
summary = {'unpacked': 0, 'profiled': 0}

for log in os.listdir('log'):
    uuid = log.split('.')[0]
    if uuid == 'salamander':
        continue

    rows[uuid] = {}

    log_path = os.path.join('log', log)

    # 1. whether this firmware can be unpacked
    unpacked = True
    profiled = False

    with open(log_path) as f:
        for line in f:
            if line.find('cannot unpack this firmware of nonstandard format') != -1:
                unpacked = False
            if line.find('migrate from') != -1:
                profiled = True
    rows[uuid]['unpacked'] = unpacked
    rows[uuid]['profiled'] = profiled
    if unpacked:
        summary['unpacked'] += 1
    if profiled:
        summary['profiled'] += 1

    pt.add_row([uuid, rows[uuid]['unpacked'], rows[uuid]['profiled']])
pt.add_row([
    'sum',
    '{:.2f}% ({}/{})'.format(summary['unpacked']/len(rows)*100, summary['unpacked'], len(rows)),
    '{:.2f}% ({}/{})'.format(summary['profiled']/len(rows)*100, summary['profiled'], len(rows)),
])

print(pt)

