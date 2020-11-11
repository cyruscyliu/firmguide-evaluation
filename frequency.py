#!/usr/bin/python
import os
import json
import argparse

from firmware import DatabaseFirmadyne
from prettytable import PrettyTable


INPUT = 'firmware.firmadyne'


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


def frequency(args):
    db = DatabaseFirmadyne(INPUT, kernel_extracted=False, brand='openwrt')

    mapping = json.load(open('target-board-properties.json'))
    summary = {}

    malurls = []
    for firmware in db.get_firmware():
        url = firmware['url']
        revision, target, subtarget = parse_openwrt_url(url)

        if target in [None, 'default']:
            malurls.append(url)
            continue

        if target not in summary:
            summary[target] = {'count': 0, 'subtarget': {}}
        summary[target]['count'] += 1

        if subtarget is None:
            subtarget = 'generic'

        if subtarget not in summary[target]['subtarget']:
            summary[target]['subtarget'][subtarget] = {'count': 0}
        summary[target]['subtarget'][subtarget]['count'] += 1

    sum2 = 0
    for k, v in summary.items():
        sum2 += v['count']

    table = PrettyTable()
    table.title = 'target/board summary on {}'.format(INPUT)
    table.field_names = [
        'target', 'subtarget',
        'arch', 'board', 'dt', 'smp', 'gic', 'uart', 'nvram',
        'count', 'portion', 'sum', 'subportion', 'subsum']
    for target, v in summary.items():
        sum1 = v['count']
        for subtarget, sv in v['subtarget'].items():
            try:
                c = sv['count']
                p1 = '{:.4f}%'.format(c * 100 / sum1)
                p2 = '{:.4f}%'.format(c * 100 / sum2)
                table.add_row([
                    target, subtarget,
                    mapping[target]['arch'], mapping[target]['board'], mapping[target]['dt'],
                    mapping[target]['smp'], mapping[target]['intc'], mapping[target]['serial'], 'unk',
                    c, p2, sum2, p1, sum1])
            except KeyError as e:
                table.add_row([
                    target, subtarget,
                    'unk', 'unk', 'unk', 'unk', 'unk', 'unk', 'unk',
                    c, p2, sum2, p1, sum1])

    if args.json:
        print(table.get_json_string(sortby='count', reversesort=True))
    elif args.csv:
        print(table.get_csv_string(sortby='count', reversesort=True))
    else:
        print(table.get_string(sortby='count', reversesort=True))
        print('cannot recognize these urls')
        for url in malurls:
            print(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)

    args = parser.parse_args()
    frequency(args)
