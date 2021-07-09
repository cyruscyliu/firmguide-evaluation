#!/usr/bin/python
import os
import yaml
import datetime
import argparse

from soc_latest import soc_dict, BUILD
from online import gen_image_list
from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.compatible import find_compatible_in_fdt
from prettytable import PrettyTable


summary = {}

def soc_statistics(target_dir, image_list):
    skipped = 0
    soc_c = 0
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        path_to_dtb = profile['components']['path_to_dtb']
        if path_to_dtb is None:
            skipped += 1
            continue
        dts = load_dtb(path_to_dtb)
        compatible = find_compatible_in_fdt(dts)
        soc = None
        for cmptbl in compatible:
            if cmptbl in soc_dict:
                soc = soc_dict[cmptbl]
                break
        if soc is None:
            print('[-] unknown soc of {}'.format(compatible))
            continue
        if soc not in summary:
            summary[soc] = []
            soc_c += 1
            print('== possible soc {} in {}'.format(soc, compatible))
        summary[soc].append(profile['statistics']['mrm'])
    print('[+] Found {} socs'.format(soc_c))
    return skipped


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
            print('[-] Generating {} images'.format(len(image_list)))
            soc_statistics(target_dir, image_list)
    with open('soc-typeii-statistics.yaml', 'w') as f:
        yaml.safe_dump(summary, f)
    print('[-] soc typeii statistics saved as soc-typeii-statistics.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)
    parser.add_argument('-s', '--select', help='Assign a particular target/subtarget, such as oxnas/generic.')

    args = parser.parse_args()
    soc(args)
