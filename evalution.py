#!/usr/bin/python

"""
This is the evaluation code of salamander.
"""
import os
import argparse

from firmware import DatabaseText, DatabaseFirmadyne


def generate_commands(args):
    if args.database_type == 'text':
        db = DatabaseText('firmware.text')
    else:
        db = DatabaseFirmadyne('firmware.firmadyne')
    for firmware in db.get_firmware():
        # fix path to firmware blob /mnt/salamander/firmware
        firmware['path'] = os.path.join('/mnt/salamander/firmware', os.path.basename(firmware['path']))
        # precise control
        if args.uuid is not None and firmware['uuid'] not in args.uuid:
            continue
        if args.limit and firmware['id'] > args.limit:
            continue
        command = './salamander.py -f {} -u {} -a {} -e {} -b {}'.format(
            firmware['path'], firmware['uuid'], firmware['arch'], firmware['endian'], firmware['brand'])
        if 'source_code' in firmware:
            command += ' -s {}'.format(firmware['source_code'])
        if args.quick:
            command += ' -q'
        if args.working_directory:
            command += ' -wd {}'.format(args.working_directory)
        print(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-wd', '--working_directory', help='assign the working directory for getting metadata, by default /tmp or %%TEMP%%')
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='text', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    generate_commands(args)
