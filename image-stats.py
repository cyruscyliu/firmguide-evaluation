#!/usr/bin/python3
import argparse

from images.firmware import DatabaseText, DatabaseFirmadyne


def dist(args):
    if args.database_type == 'text':
        db = DatabaseText('images/firmware.text')
    else:
        db = DatabaseFirmadyne('images/firmware.firmadyne')

    distribution = {}
    for firmware in db.get_firmware():
        brand = firmware['brand']
        arch = firmware['arch']
        endian = firmware['endian']

        if arch is None:
            arch = 'unknown'
        if endian is None:
            endian = 'unknown'

        if brand not in distribution:
            distribution[brand] = {}
        if arch not in distribution[brand]:
            distribution[brand][arch] = {}
        if endian not in distribution[brand][arch]:
            distribution[brand][arch][endian] = 0
        distribution[brand][arch][endian] += 1

    # arch distritbuion
    arch = []
    for k, v in distribution.items():
        for a in v:
            if a not in arch:
                arch.append(a)
    # header
    header = ['brand']
    for a in arch:
        for e in ['b', 'l', 'unknown']:
            header.append(a+e)
    print(','.join(header))

    for k, v in distribution.items():
        output = [k]
        for a in arch:
            if a in v:
                for e in ['b', 'l', 'unknown']:
                    if e in v[a]:
                        output.append(v[a][e])
                    else:
                        output.append(0)
            else:
                output.append(0)
                output.append(0)
                output.append(0)
        print(','.join([str(i) for i in output]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dbt', '--database_type', choices=['text', 'firmadyne'], default='firmadyne', type=str)
    parser.add_argument('-l', '--limit', type=int, default=0, help='limit the amount of firmware to test')
    parser.add_argument('-u', '--uuid', type=str, nargs='+', help='assign a or several firmware to tested')
    parser.add_argument('-q', '--quick', action='store_true', default=False, help='disable tracing and diagnosis')
    args = parser.parse_args()
    dist(args)
