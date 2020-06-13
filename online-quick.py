#!/usr/bin/python
import os
import yaml
import datetime
import argparse

from prettytable import PrettyTable
from online import find_format, find_kernel_extracted, find_match, \
        find_prepare, find_rootfs, find_user_space, find_shell, \
        find_time, gen_image_list


BUILD = '/root/build-latest'


def online(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = [
        'TARGET', 'SUBTARGET', 'FORMAT', 'KERNEL_EXTRACTED', 'MATCH',
        'PREPARE', 'ROOTFS', 'USER_SPACE', 'SHELL', 'TIME'
    ]

    for target, v in results.items():
        for subtarget, vv in v.items():
            if argv.select is not None:
                if '{}/{}'.format(target, subtarget) != argv.select:
                    continue
            target_dir = os.path.join(BUILD, vv['hash'])
            image_list = gen_image_list(target, subtarget, target_dir)
            unpack_format = find_format(target_dir, image_list)
            unpack_kernel_extracted = \
                find_kernel_extracted(target_dir, image_list)
            match = find_match(target_dir, image_list)
            prepare = find_prepare(target_dir, image_list)
            boot_rootfs, failed_rootfs = find_rootfs(target_dir, image_list)
            boot_user_space = find_user_space(target_dir, image_list)
            boot_shell, failed_shell = find_shell(target_dir, image_list)
            time = find_time(target_dir, image_list)
            line = [target, subtarget, unpack_format, unpack_kernel_extracted,
                    match, prepare, '{}({})'.format(boot_rootfs, failed_rootfs),
                    boot_user_space, '{}({})'.format(boot_shell, failed_shell),
                    '{:.2f}'.format(time)]
            table.add_row(line)

    if args.json:
        print(table.get_json_string())
    elif args.csv:
        print(table.get_csv_string())
    else:
        print(table.get_string())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)
    parser.add_argument('-s', '--select', help='Assign a particular target/subtarget, such as oxnas/generic.')

    args = parser.parse_args()
    online(args)
