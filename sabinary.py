#!/usr/bin/python

"""
slbin commands generator
input: firmware.text/firmadyne
output: slbin commands
"""
import os
import json
import argparse

from firmware import DatabaseText, DatabaseFirmadyne
from frequency import parse_openwrt_url

mapping = json.load(open('openwrt_target_maps_latest_kernel_version.json'))

FIRMWARE_BINARY = '/root/images'
SALAMANDER = '/root/esv'


def generate_commands(args):
    summary_commands = []
    if args.database_type == 'text':
        db = DatabaseText('firmware.text')
    else:
        db = DatabaseFirmadyne('firmware.firmadyne')

    for firmware in db.get_firmware():
        firmware['path'] = os.path.join(FIRMWARE_BINARY, os.path.basename(firmware['path']))

        # precise control
        if args.uuid is not None and firmware['uuid'] not in args.uuid:
            continue
        if args.limit and firmware['id'] > args.limit:
            continue

        # arch/endian
        archm, endianm = None, None
        if 'url' in firmware:
            url = firmware['url']
            _, target, _ = parse_openwrt_url(url)
            if target in mapping:
                archm = mapping[target]['arch']
                endianm = mapping[target]['endian']

        arch = firmware['arch']
        endian = firmware['endian']

        comment = False
        if arch is None:
            if archm is not None:
                arch = archm
            else:
                comment = True
        if endian is None:
            if endianm is not None:
                endian = endianm
            else:
                comment = True

        if comment:
            command = '# cd {} && ./bin.py -f {} -u {} -a {} -e {} -b {}'.format(
                SALAMANDER, firmware['path'], firmware['uuid'],
                arch, endian, firmware['brand'])
        else:
            command = 'cd {} && ./bin.py -f {} -u {} -a {} -e {} -b {}'.format(
                SALAMANDER, firmware['path'], firmware['uuid'],
                arch, endian, firmware['brand'])

        if 'url' in firmware:
            command += ' -l {}'.format(firmware['url'])

        command += ' && cd ~-'
        print(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='text', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    generate_commands(args)
