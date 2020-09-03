#!/usr/bin/python
import os
import yaml
import datetime
import argparse

from prettytable import PrettyTable
from online import gen_image_list


BUILD = '/root/build-latest'


def __find_now(line):
    now = ' '.join(line.split()[:2])
    now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S,%f')
    return now


def find_boottime(target_dir, log):
    start, end = None, None
    shell = False
    with open(log) as f:
        for line in f:
            # 2020-08-03 09:55:27,450 - INFO - QEMUController - tracing - Uncompressing Linux... done, booting the kernel.
            if start is None and line.find('QEMUController') != -1:
                start = __find_now(line)
            elif start is not None and line.find('QEMUController') != -1:
                end = __find_now(line)

            if line.find('Welcome to Buildroot') != -1:
                shell = True
                break

    if shell:
        return (end.timestamp() - start.timestamp())
    else:
        return None


def online(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = [
        'Target', 'Subtarget', 'IMAGE', 'REALBOOT'
    ]

    for target, v in results.items():
        for subtarget, vv in v.items():
            if argv.select is not None:
                if '{}/{}'.format(target, subtarget) != argv.select:
                    continue
            target_dir = os.path.join(BUILD, vv['hash'])
            image_list = gen_image_list(target, subtarget, target_dir)
            for k, v in image_list.items():
                log = os.path.join(target_dir, v['log'])
                boottime = find_boottime(target_dir, log)
                if boottime is None:
                    continue
                table.add_row([target, subtarget, os.path.basename(log), boottime])

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
