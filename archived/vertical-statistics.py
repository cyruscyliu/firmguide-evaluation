#!/usr/bin/python
import os
import json
import argparse

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.cpu import find_flatten_cpu_in_fdt
from slcore.dt_parsers.serial import find_flatten_serial_in_fdt
from slcore.dt_parsers.intc import find_flatten_intc_in_fdt
from slcore.dt_parsers.timer import find_flatten_timer_in_fdt


# we only check all subtargets in 19.07.1 and ramips rt305x from 14.07
verticals = [
    'openwrt-dtb-only/archive/14.07/targets/ramips/rt305x',
    'openwrt-dtb-only/archive/15.05/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.1/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.0/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.2/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.4/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.3/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.5/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.6/targets/ramips/rt305x',
    'openwrt-dtb-only/release/17.01.7/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.1/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.3/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.4/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.5/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.6/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.7/targets/ramips/rt305x',
    'openwrt-dtb-only/release/18.06.0/targets/ramips/rt305x',
    'openwrt-dtb-only/release/19.07.0/targets/ramips/rt305x',
    'openwrt-dtb-only/release/19.07.1/targets/ramips/rt305x',
]


def pol(args):
    # table = PrettyTable()
    c_all = {}

    n = 0
    for vertical in verticals:
        for root, dirs, files in os.walk(vertical):
            for dtb in files:
                print('{:04}'.format(n), dtb)
                subtarget = 'rt305x'
                if subtarget not in c_all:
                    c_all[subtarget] = {}
                version = root.split('/')[2]
                if version not in c_all[subtarget]:
                    c_all[subtarget][version] = []

                try:
                    dts = load_dtb(os.path.join(root, dtb))
                    cpus = find_flatten_cpu_in_fdt(dts)
                    if cpus is None:
                        cpus = []
                    intcs = find_flatten_intc_in_fdt(dts)
                    if intcs is None:
                        intcs = []
                    timers = find_flatten_timer_in_fdt(dts)
                    if timers is None:
                        timers = []
                    serials = find_flatten_serial_in_fdt(dts)
                    if serials is None:
                        serials = []
                except Exception as e:
                    print('>>>> ERROR <<<< {} in {}'.format(e, os.path.join(root, dtb)))
                    n += 1
                    continue

                a = {'cpus': [], 'intcs': [], 'timers': [], 'serials': []}
                for c in cpus:
                    if c['compatible'] not in a['cpus']:
                        a['cpus'].append(c['compatible'])
                for i in intcs:
                    if i['compatible'] not in a['intcs']:
                        a['intcs'].append(i['compatible'])
                for t in timers:
                    if t['compatible'] not in a['timers']:
                        a['timers'].append(t['compatible'])
                for s in serials:
                    if s['compatible'] not in a['serials']:
                        a['serials'].append(s['compatible'])
                c_all[subtarget][version].append(a)
                n += 1

    with open('vertical-statistics.json', 'w') as f:
        json.dump(c_all, f, indent=4, sort_keys=True)
    print('save as vertical-statistics.json')

    # if args.json:
        # print(table.get_json_string(sortby='count', reversesort=True))
    # elif args.csv:
        # print(table.get_csv_string(sortby='count', reversesort=True))
    # else:
        # print(table.get_string(sortby='count', reversesort=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)

    args = parser.parse_args()
    pol(args)
