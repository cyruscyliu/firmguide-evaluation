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


def find_timeline(target_dir, log):
    status = 0 # IDEL
    timeline = {}
    shell = None
    with open(log) as f:
        for line in f:
            if status == 0 and line.find('- unpack -') != -1:
                status = 1 # UNPACK
                timeline[status] = __find_now(line)
            elif status == 1 and line.find('- msearch -') != -1:
                status = 2 # MSEARCH
                timeline[status] = __find_now(line)
            elif status == 2 and line.find('- preparation -') != -1:
                status = 3 # PREPARATION
                timeline[status] = __find_now(line)
            elif status == 3 and line.find('- tracing -') != -1:
                status = 4 # TRACING
                timeline[status] = __find_now(line)
            elif status == 4 and line.find('- loadtrace -') != -1:
                status = 5 # LOAD_TRACE
                timeline[status] = __find_now(line)
            elif status == 5 and line.find('- fastuserlevel -') != -1:
                status = 6 # FASTUSERLEVEL
                timeline[status] = __find_now(line)
            elif status == 6 and line.find('- deltrace -') != -1:
                status = 7 # DELTRACE
                timeline[status] = __find_now(line)
            elif status == 2 and line.find('- snapshot -') != -1:
                status = 8 # SUMMARY
                timeline[status] = __find_now(line)
            elif status == 6 and line.find('- snapshot -') != -1:
                status = 8 # SUMMARY
                timeline[status] = __find_now(line)
            elif status == 7 and line.find('- snapshot -') != -1:
                status = 8 # SUMMARY
                timeline[status] = __find_now(line)
            elif status == 8 and line.find('source at') != -1:
                timeline[status] = __find_now(line)

            if line.find('Welcome to Buildroot') != -1:
                shell = __find_now(line)

    timeline_list = []
    for i in range(1, 9):
        if i not in timeline:
            timeline_list.append(timeline_list[i - 2])
        else:
            timeline_list.append((timeline[i] - timeline[1]).total_seconds())

    timeline_list_diff = []
    for i in range(0, len(timeline_list) - 1):
        timeline_list_diff.append(timeline_list[i + 1] - timeline_list[i])

    if shell is not None:
        timeline_list_diff.append((shell - timeline[4]).total_seconds())
    else:
        timeline_list_diff.append(None)

    return timeline_list_diff


def online(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = [
        'IMAGE', 'UNPACK', 'MSEARCH', 'PREPARE', 'TRACE',
        'LOAD_TRACE', 'USERLEVEL', 'SUMMARY', 'SHELL'
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
                print(log)
                timeline = find_timeline(target_dir, log)
                if timeline[3] == .0 or timeline[-1] is None:
                    continue
                table.add_row([os.path.basename(log)] + timeline)

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
    parser.add_argument('-m', '--mode', help='Timeline mode', choices=['online', 'offline'], default='online')

    args = parser.parse_args()
    online(args)
