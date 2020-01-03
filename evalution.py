#!/usr/bin/python

"""
This is the evaluation code of salamander.
"""
import os
import argparse

from firmware import DatabaseText, DatabaseFirmadyne

FIRMWARE_BINARY = '/mnt/salamander/firmwware'
SRCODE = '/mnt/salamander/srcode'


def generate_commands(args):
    if args.database_type == 'text':
        db = DatabaseText('firmware.text')
    else:
        db = DatabaseFirmadyne('firmware.firmadyne')
    for firmware in db.get_firmware():

        # fix path to firmware blob /mnt/salamander/firmware
        firmware['path'] = os.path.join(FIRMWARE_BINARY, os.path.basename(firmware['path']))
        paths = [firmware['path'], ]
        # precise control
        if args.uuid is not None and firmware['uuid'] not in args.uuid:
            continue
        if args.limit and firmware['id'] > args.limit:
            continue
        command = './salamander.py'
        command += ' -u {} -a {} -e {} -b {}'.format(
            firmware['uuid'], firmware['arch'], firmware['endian'], firmware['brand'])

        srcode_summary = os.path.join('summary', '{}.summary'.format(firmware['uuid']))
        if os.path.exists(srcode_summary):
            with open(srcode_summary) as f:
                for line in f:
                    uuid, label, value = line.split('\t')
                    if label == 'source code':
                        command += ' -s {}'.format(os.path.join(SRCODE, value.strip()))
                    if label == 'firmware':
                        paths.append(os.path.join(SRCODE, value.strip()))
        if args.quick:
            command += ' -q'
        if args.working_directory:
            command += ' -wd {}'.format(args.working_directory)

        for path in paths:
            cmd = command + ' -f {}'.format(path)
            print(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-wd', '--working_directory',
                        help='assign the working directory for getting metadata, by default /tmp or %%TEMP%%')
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='text', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    generate_commands(args)
