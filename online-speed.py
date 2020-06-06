#!/usr/bin/python
import os
import yaml
import datetime
import argparse
from prettytable import PrettyTable
from online import gen_image_list


BUILD = '/root/build-latest'

def datetime_to_string(t):
    return datetime.datetime.strftime(t + datetime.timedelta(hours=8), '%m-%d %H:%M:%S')


def find_start_and_end(target_dir, image_list):
    start = datetime.datetime.strptime('3000-12-31 23:59:59,999', '%Y-%m-%d %H:%M:%S,%f')
    end = datetime.datetime.strptime('2000-12-31 23:59:59,999', '%Y-%m-%d %H:%M:%S,%f')
    for k, v in image_list.items():
        log = os.path.join(target_dir, v['log'])
        with open(log) as f:
            for line in f:
                now = ' '.join(line.split()[:2])
                try:
                    now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S,%f')
                except ValueError:
                    continue
                if now < start:
                    start = now
                if now > end:
                    end = now
    return start, end


def online_speed(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = ['TARGET', 'SUBTARGET', 'START', 'END', 'COUNT', 'TIME']

    for target, v in results.items():
        for subtarget, vv in v.items():
            if argv.select is not None:
                if '{}/{}'.format(target, subtarget) != argv.select:
                    continue
            target_dir = os.path.join(BUILD, vv['hash'])
            image_list = gen_image_list(target, subtarget, target_dir)
            start, end = find_start_and_end(target_dir, image_list)
            line = [target, subtarget, datetime_to_string(start), datetime_to_string(end),
                    len(image_list), end - start]
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
    online_speed(args)
