#!/usr/bin/python

"""
slsrc commands generator
input: firmware.text/firmware.firmadyne
input: openwrt_target_maps_latest_kernel_version
output: slsrc commands
"""
import os
import json
import argparse

from firmware import DatabaseText, DatabaseFirmadyne
from frequency import parse_openwrt_url

SRCODE = '/root/openwrt-build-docker'

all_distinct_srcode = []
mapping = json.load(open('openwrt_target_maps_latest_kernel_version.json'))

def generate_commands(args):
    summary_commands = []
    if args.database_type == 'text':
        db = DatabaseText('firmware.text')
    else:
        db = DatabaseFirmadyne('firmware.firmadyne')

    for firmware in db.get_firmware():
        # precise control
        if args.uuid is not None and firmware['uuid'] not in args.uuid:
            continue
        if args.limit and firmware['id'] > args.limit:
            continue

        # board
        if 'url' not in firmware:
            continue
        url = firmware['url']
        _, target, _ = parse_openwrt_url(url)
        if target in mapping:
            board = mapping[target]['target']
            archm = mapping[target]['arch']
            endianm = mapping[target]['endian']
        else:
            continue

        # arch/endian
        arch = firmware['arch']
        endian = firmware['endian']
        if arch is None:
            arch = archm
        # assert arch == archm, '{} != {} in {}'.format(arch, archm, url)
        if endian is None:
            endian = endianm
        # assert endian == endianm, '{} != {} in {}'.format(endian, endianm, url)

        command = './slsrc.py -u {}'.format(board)
        command += ' -a {} -e {} -b {}'.format(arch, endian, firmware['brand'])

        srcode_summary = os.path.join('summary', '{}.summary'.format(firmware['uuid']))
        if os.path.exists(srcode_summary):
            with open(srcode_summary) as f:
                # only 1 line
                things = f.readline().strip().split(',')
                srcode_value = things[6]
                if len(srcode_value):
                    command += ' -s {}'.format(os.path.join(SRCODE, srcode_value.strip()))
                    if srcode_value in all_distinct_srcode:
                        continue
                    all_distinct_srcode.append(srcode_value)
                else:
                    continue
                makeout_value = things[9]
                if len(makeout_value):
                    command += ' -mkout {}'.format(os.path.join(SRCODE, makeout_value))
                gcc_value = things[10]
                if len(gcc_value):
                    command += ' -gcc {}'.format(os.path.join(SRCODE, gcc_value[:-3]))
                binary_value = things[11]
                if len(binary_value):
                    command += ' -f {}'.format(os.path.join(SRCODE, binary_value))
                else:
                    continue
        else:
            continue

        print(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='text', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    args = parser.parse_args()
    generate_commands(args)

