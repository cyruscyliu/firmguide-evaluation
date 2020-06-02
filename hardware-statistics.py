#!/usr/bin/python
import os
import argparse

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.cpu import find_flatten_cpu_in_fdt
from slcore.dt_parsers.serial import find_flatten_serial_in_fdt
from slcore.dt_parsers.intc import find_flatten_intc_in_fdt
from slcore.dt_parsers.timer import find_flatten_timer_in_fdt
from slcore.dt_parsers.flash import find_flatten_flash_in_fdt
from slcore.dt_parsers.misc import find_flatten_misc_in_fdt
from slcore.dt_parsers.memory import find_flatten_ram_in_fdt
from slcore.dt_parsers.mmio import find_flatten_mmio_in_fdt, \
    merge_flatten_mmio
from slcore.brick import Brick


def hardware(args):
    c_all = []
    i = 1

    c_existing = {}
    if os.path.exists('hardware-statistics.txt'):
        with open('hardware-statistics.txt') as f:
            for line in f:
                dtb, c = line.strip().split(',')
                c_existing[dtb] = c

    for dtb in os.listdir('dtb'):
        print('{:04}'.format(i), dtb)
        if dtb in c_existing:
            c = c_existing[dtb]
            c_all.append((dtb, c))
            i += 1
            continue

        c = 0
        dts = load_dtb(os.path.join('dtb', dtb))
        skip = []

        hardware = []
        try:
            cpus = find_flatten_cpu_in_fdt(dts)
            if cpus is not None:
                c += len(cpus)
            rams = find_flatten_ram_in_fdt(dts)
            if rams is not None:
                c += len(rams)
            miscs = find_flatten_misc_in_fdt(dts)
            if miscs is not None:
                c += len(miscs)
                hardware.extend(miscs)
            intcs = find_flatten_intc_in_fdt(dts)
            if intcs is not None:
                c += len(intcs)
                hardware.extend(intcs)
            timers = find_flatten_timer_in_fdt(dts)
            if timers is not None:
                c += len(timers)
                hardware.extend(timers)
            serials = find_flatten_serial_in_fdt(dts)
            if serials is not None:
                c += len(serials)
                hardware.extend(timers)
            flashes = find_flatten_flash_in_fdt(dts)
            if flashes is not None:
                c += len(flashes)
                hardware.extend(flashes)

            for hw in hardware:
                skip.append(hw['compatible'])

            mmios = find_flatten_mmio_in_fdt(dts)
            mmios = merge_flatten_mmio(mmios)
            for mmio in mmios:
                if mmio['compatible'] in skip:
                    continue
                else:
                    c += 1
            c_all.append((dtb, c))
        except Exception as e:
            print('>>>> ERROR <<<< {}'.format(e))
        i += 1

    with open('hardware-statistics.txt', 'w') as f:
        for c in c_all:
            f.write('{},{}\n'.format(c[0], c[1]))
    print('save as hardware-statistics.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    # parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)

    args = parser.parse_args()
    hardware(args)
