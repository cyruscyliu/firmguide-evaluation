#!/usr/bin/python
import os
import fdt
import argparse


def fragmentation(device_tree_blob):
    with open(device_tree_blob, 'rb') as f:
        dtb = f.read()
        dts = fdt.parse_dtb(dtb)

    num_of_hardware = 0
    for path, nodes, properties in dts.walk():
        if dts.exist_property('compatible', path):
            num_of_hardware += 1

    return num_of_hardware


def f_for_all(path):
    statistics = [0, 0]
    for root, dirs, files in os.walk(path):
        for file_ in files:
            full_path = os.path.join(root, file_)
            count = fragmentation(full_path)
            statistics[0] += 1
            statistics[1] += count
    return statistics


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-dtb', help='device tree blob')
    parser.add_argument('-path', help='device tree blob repo')
    args = parser.parse_args()

    if args.dtb:
        print(fragmentation(args.dtb))
    elif args.path:
        print(f_for_all(os.path.realpath(args.path)))
