#!/usr/bin/python
"""
target/board summary on firmware.firmdyne.xxxxx

input: firmadyne.firmware database
output: target: openwrt target
output: count: count of the target in the database
output: arch: arch of the target
outout: board: kernel board r.s.t the target
output: propertion: propertion of the target in the database
output: kernel_extracted: propertion of kernel extracted firmware
"""
import os
import sys
import json

from firmware import DatabaseText, DatabaseFirmadyne
from prettytable import PrettyTable


INPUT = 'firmware.firmadyne.91600'

def parse_openwrt_url(url):
    homepage = os.path.dirname(url)

    items = homepage.split('/')
    revision = items[4]
    target = items[5]
    subtarget = None

    if len(items) > 6:
        subtarget = items[6]

    if target in ['targets']:
        target = subtarget
        subtarget = items[7]

    return revision, target, subtarget

def frequency(argv):
    summary_commands = []
    db = DatabaseFirmadyne(INPUT, kernel_extracted=False, brand='openwrt')

    mapping = json.load(open('openwrt_target_maps_latest_kernel_version.json'))
    summary = {}

    malurls = []
    for firmware in db.get_firmware():
        url = firmware['url']
        revision, target, subtarget = parse_openwrt_url(url)

        if target in [None, 'default']:
            malurls.append(url)
            continue

        if target in summary:
            summary[target]['count'] += 1
        else:
            summary[target] = {'count':1, 'kernel_extracted':0}
        if firmware['kernel_extracted']:
            summary[target]['kernel_extracted'] += 1

    firmware_sum = 0
    for k, v in summary.items():
        firmware_sum += v['count']

    kernel_extracted_sum = 0
    for k, v in summary.items():
        kernel_extracted_sum += v['kernel_extracted']

    table = PrettyTable()
    table.title = 'target/board summary on {}'.format(INPUT)
    table.field_names = ['target', 'count', 'arch', 'board', 'propertion', 'kernel_extracted']
    for k, v in summary.items():
        count = v['count']
        p =  '{:.4f}% ({}/{})'.format(count/firmware_sum, count, firmware_sum)
        kernel_extracted =  '{:.4f}% ({}/{})'.format(v['kernel_extracted']/kernel_extracted_sum, v['kernel_extracted'], kernel_extracted_sum)
        try:
            table.add_row([k, count, mapping[k]['arch'], mapping[k]['target'], p, kernel_extracted])
        except KeyError:
            table.add_row([k, count, 'unknown', 'unknown', p, kernel_extracted])

    if len(argv) == 2 and argv[1] == '-j':
        print(table.get_json_string(sortby='count', reversesort=True))
        return
    print(table.get_string(sortby='count', reversesort=True))
    print('cannot recognize these urls')
    for url in malurls:
        print(url)

if __name__ == "__main__":
    frequency(sys.argv)

