#!/usr/bin/python
"""
download commands generator
input: firmware.text/firmadyne
output: download commands
"""
import os
import argparse

from firmware import DatabaseText, DatabaseFirmadyne


FIRMWARE_BINARY = '/root/images'
FIRMWARE_REMOTE = '/mnt/firm/original_image'
REMOTE = '-i id_rsa cloud@192.168.1.218'


def generate_commands(args):
    if args.database_type == 'text':
        db = DatabaseText('firmware.text')
    else:
        db = DatabaseFirmadyne('firmware.firmadyne.91600', brand='openwrt')

    for firmware in db.get_firmware():
        from_path = os.path.join(FIRMWARE_REMOTE, firmware['path'])
        to_path = os.path.join(FIRMWARE_BINARY, os.path.basename(firmware['path']))

        # precise control
        if args.uuid is not None and firmware['uuid'] not in args.uuid:
            continue
        if args.limit and firmware['id'] > args.limit:
            continue

        command = 'scp {}:{} {}'.format(REMOTE, from_path, to_path)
        print(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='firmadyne', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    generate_commands(args)
