#!/usr/bin/python3
import os
import json
import argparse

from images.firmware import DatabaseText, DatabaseFirmadyne, parse_openwrt_url

mapping = json.load(open('target-board-properties.json'))

FIRMWARE_BINARY = '/root/images'
FIRMGUIDE = '/root/esv-latest'


def generate_commands(args):
    if args.database_type == 'text':
        db = DatabaseText('images/firmware.text')
    else:
        db = DatabaseFirmadyne('images/firmware.firmadyne', brand='openwrt')

    for firmware in db.get_firmware():
        firmware['path'] = \
            os.path.join(FIRMWARE_BINARY, os.path.basename(firmware['path']))

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
            if target in mapping and 'arch' in mapping[target]:
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
            command = '# cd {} && ./firmware upload -f {}'.format(
                FIRMGUIDE, firmware['path'])
        else:
            command = 'cd {} && ./firmguide upload -f {}'.format(
                FIRMGUIDE, firmware['path'])

        if 'url' in firmware:
            command += ' -l {}'.format(firmware['url'])
        command += ' -nc'
        command += ' -to 120'
        command += ' -del'
        print(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='text', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    generate_commands(args)
