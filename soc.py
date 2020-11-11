#!/usr/bin/python
import os
import yaml
import datetime
import argparse

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.compatible import find_compatible_in_fdt
from slcore.dt_parsers.intc import find_flatten_intc_in_fdt
from slcore.dt_parsers.timer import find_flatten_timer_in_fdt
from prettytable import PrettyTable
from online import gen_image_list


BUILD = '/root/build-latest'

summary = {}

def soc_statistics(target_dir, image_list):
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        path_to_dtb = profile['components']['path_to_dtb']
        if path_to_dtb is None:
            continue
        dts = load_dtb(path_to_dtb)
        compatible = find_compatible_in_fdt(dts)
        compatible_str = '@'.join(compatible)
        intcs = find_flatten_intc_in_fdt(dts)
        timers = find_flatten_timer_in_fdt(dts)
        if compatible_str not in summary:
            summary[compatible_str] = {'intc': [], 'timer': []}
        for intc in intcs:
            c = intc['compatible']
            if c not in summary[compatible_str]['intc']:
                summary[compatible_str]['intc'].append('@'.join(c))
        for timer in timers:
            c = timer['compatible']
            if c not in summary[compatible_str]['timer']:
                summary[compatible_str]['timer'].append('@'.join(c))
        if 'images' not in summary[compatible_str]:
            summary[compatible_str]['images'] = {}
        summary[compatible_str]['images'][k] = v
        summary[compatible_str]['target_dir'] = target_dir


def soc(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = [
        'TARGET', 'SUBTARGET', 'SUM', 'FORMAT', 'KERNEL_EXTRACTED', 'MATCH',
        'PREPARE', 'ROOTFS', 'USER_SPACE', 'SHELL', 'TIME'
    ]

    print('[-] Please wait, it takes time ...')
    for target, v in results.items():
        for subtarget, vv in v.items():
            if argv.select is not None:
                if '{}/{}'.format(target, subtarget) != argv.select:
                    continue
            print('[-] Handling {}/{}'.format(target, subtarget))
            target_dir = os.path.join(BUILD, vv['hash'])
            image_list = gen_image_list(target, subtarget, target_dir)
            soc_statistics(target_dir, image_list)
    with open('soc-statistics.yaml', 'w') as f:
        yaml.safe_dump(summary, f)
    print('[-] soc statistics saved as soc-statistics.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)
    parser.add_argument('-s', '--select', help='Assign a particular target/subtarget, such as oxnas/generic.')

    args = parser.parse_args()
    soc(args)
