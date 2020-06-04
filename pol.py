#!/usr/bin/python
import os
import json
import argparse

from prettytable import PrettyTable
from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.cpu import find_flatten_cpu_in_fdt
from slcore.dt_parsers.serial import find_flatten_serial_in_fdt
from slcore.dt_parsers.intc import find_flatten_intc_in_fdt
from slcore.dt_parsers.timer import find_flatten_timer_in_fdt


# we only check all subtargets in 19.07.1 and ramips rt305x from 14.07
horizontal = 'openwrt-dtb-only/release/19.07.1/targets'


def pol(args):
    # table = PrettyTable()
    c_all = {}

    for root, dirs, files in os.walk(horizontal):
        for dtb in files:
            target = root.split('/')[0]
            if target not in c_all:
                c_all[target] = {}
            subtarget = root.split('/')[1]
            if subtarget not in c_all[target]:
                c_all[target][subtarget] = []

            try:
                dts = load_dtb(os.path.join(root, dtb))
                cpus = find_flatten_cpu_in_fdt(dts)
                intcs = find_flatten_intc_in_fdt(dts)
                timers = find_flatten_timer_in_fdt(dts)
                serials = find_flatten_serial_in_fdt(dts)
            except Exception as e:
                print('>>>> ERROR <<<< {} in {}'.format(e, os.path.join(root, dtb)))

            a = {'cpus': cpus, 'intcs': intcs, 'timers': timers, 'serials': serials}
            c_all[target][subtarget].append(a)

    with open('horizontal-similarity.json', 'w') as f:
        json.dump(c_all, f, indent=4, sort_keys=True)
    print('save as horizontal-similarity.json')

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
