#!/usr/bin/python3
import argparse

from images.firmware import DatabaseText, DatabaseFirmadyne


def dist(args):
    if args.database_type == 'text':
        db = DatabaseText('images/firmware.text')
    else:
        db = DatabaseFirmadyne('images/firmware.firmadyne', brand='openwrt')

    distribution = {}
    for firmware in db.get_firmware():
        kv = firmware['kernel_version']
        if kv == '':
            kv = 'unknown'
        if kv not in distribution:
            distribution[kv] = 0
        distribution[kv] += 1
    print('kernel version, count')
    for k, v in distribution.items():
        print('{},{}'.format(k, v))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='firmadyne', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    dist(args)
