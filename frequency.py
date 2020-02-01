#!/usr/bin/python
"""
target/board summary on firmware.firmdyne

input: firmadyne.firmware database
output: target: openwrt target
output: count: count of the target in the database
output: arch: arch of the target
outout: board: kernel board r.s.t the target
output: propertion: propertion of the target in the database
"""
import os
import json

from firmware import DatabaseText, DatabaseFirmadyne
from prettytable import PrettyTable


def parse_openwrt_url(url):
    homepage = os.path.dirname(url)

    items = homepage.split('/')
    revision = items[4]
    target = items[5]
    subtarget = None
    if len(items) == 8:
        subtarget = items[6]

    if target in ['targets']:
        target = subtarget

    return revision, target, subtarget

def frequency():
    summary_commands = []
    db = DatabaseFirmadyne('firmware.firmadyne')

    mapping = json.load(open('openwrt_target_maps_latest_kernel_version.json'))
    summary = {}

    for firmware in db.get_firmware():
        url = firmware['url']
        revision, target, subtarget = parse_openwrt_url(url)

        if target in summary:
            summary[target] += 1
        else:
            summary[target] = 1

    firmware_sum = 0
    for k, v in summary.items():
        firmware_sum += v

    table = PrettyTable()
    table.title = 'target/board summary on firmware.firmadyne'
    table.field_names = ['target', 'count', 'arch', 'board', 'propertion']
    for k, v in summary.items():
        p =  '{:.4f}% ({}/{})'.format(v/firmware_sum, v, firmware_sum)
        try:
            table.add_row([k, v, mapping[k]['arch'], mapping[k]['target'], p])
        except KeyError:
            table.add_row([k, v, 'unknown', 'unknown', p])

    print(table.get_string(sortby='count', reversesort=True))

if __name__ == "__main__":
    frequency()

