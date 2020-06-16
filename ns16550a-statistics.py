#!/usr/bin/python
import os
import argparse

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.serial import find_flatten_serial_in_fdt


candidates = [
    'snps,dw-apb-uart',
    'ns16550a',
    'ns16550',
    'ns8250',
]


def hardware(args):
    i = 1

    c_all = {
        'snps,dw-apb-uart': 0,
        'ns16550a': 0,
        'ns16550': 0,
        'ns8250': 0,
    }
    for root, dirs, files in os.walk('dtb'):
        for dtb in files:
            print('{:04}'.format(i), dtb)
            dts = load_dtb(os.path.join(root, dtb))

            try:
                serials = find_flatten_serial_in_fdt(dts)
                if serials is None:
                    i += 1
                    continue
                for serial in serials:
                    compatible = serial['compatible'][-1]
                    if compatible in candidates:
                        c_all[compatible] += 1
                        break
            except Exception as e:
                print('>>>> ERROR <<<< {}'.format(e))
            i += 1

    with open('ns16550a-statistics.txt', 'w') as f:
        for k, v in c_all.items():
            f.write('{},{}\n'.format(k, v))
    print('save as ns16550a-statistics.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    args = parser.parse_args()
    hardware(args)
