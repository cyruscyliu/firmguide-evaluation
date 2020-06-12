#!/usr/bin/python
import os
import json
import argparse

from firmware import DatabaseText, DatabaseFirmadyne

mapping = json.load(open('target-board-properties.json'))

FIRMWARE_BINARY = '/root/images'
SALAMANDER = '/root/esv-latest'


def generate_commands(args):
    if args.database_type == 'text':
        db = DatabaseText('firmware.text')
    else:
        if args.database_path:
            if args.brand:
                db = DatabaseFirmadyne(args.database_path, brand=args.brand)
            else:
                db = DatabaseFirmadyne(args.database_path, brand='!openwrt')
        else:
            db = DatabaseFirmadyne('firmware.firmadyne', brand='!openwrt')

    for firmware in db.get_firmware():
        firmware['path'] = \
            os.path.join(FIRMWARE_BINARY, os.path.basename(firmware['path']))

        # precise control
        if args.uuid is not None and firmware['uuid'] not in args.uuid:
            continue
        if args.limit and firmware['id'] > args.limit:
            continue

        command = 'cd {} && ./salamander upload -f {}'.format(
            SALAMANDER, firmware['path'])

        if 'url' in firmware:
            command += ' -l {}'.format(firmware['url'])
        command += ' -nc'
        # command += ' -to 120'
        command += ' -del'
        print(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='text', type=str)
    parser.add_argument('-p', '--database_path', help='database path')
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    parser.add_argument('-b', '--brand', choices=['!openwrt', 'netgear'], help='brand')
    args = parser.parse_args()
    generate_commands(args)
