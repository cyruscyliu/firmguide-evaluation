#!/usr/bin/python
import os
import yaml
import argparse

from prettytable import PrettyTable
from kernel_version import find_kernel_version_in_strings
from slcore.parser import get_candidates, get_all_strings

BUILD = '/home/liuqiang/build'


def find_openwrt_revision(target_dir, signature):
    for trace in os.listdir(target_dir):
        if not trace.endswith('trace'):
            continue
        if trace.find(signature) == -1:
            continue

        items = trace[:-6].split('-')
        if len(items) == 5:
            revision = items[0]
        elif len(items) == 6:
            revision = '-'.join(items[:2])
        else:
            revision = None

        if revision:
            return revision
    return None


def find_kernel_version(target_dir):
    profile = yaml.safe_load(open(os.path.join(target_dir, 'profile.yaml')))

    path_to_kernel = profile['components']['path_to_kernel']
    if path_to_kernel is None:
        print('kernel is None in', target_dir)
        return None
    candidates = get_candidates(path_to_kernel)
    strings = get_all_strings(candidates)
    kernel_version = find_kernel_version_in_strings(strings)

    if kernel_version:
        return kernel_version
    else:
        return None


def find_hardware_models(target_dir):
    profile = yaml.safe_load(open(os.path.join(target_dir, 'profile.yaml')))

    if 'statistics' not in profile:
        return None, None, None, None

    crm = profile['statistics']['crm']
    smm = profile['statistics']['smm']
    mrm = profile['statistics']['mrm']
    iv = profile['statistics']['iv']

    return crm, smm, mrm, iv


def find_loc(target_dir):
    summary = yaml.load(''.join(os.popen('cloc {} --yaml'.format(
        os.path.join(target_dir, 'qemu-4.0.0'))).readlines()[5:]))
    return summary['SUM']['code'] + summary['SUM']['blank'] + summary['SUM']['comment']


def find_validation(target_dir):
    return True


def offline(args):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = [
        'target', 'subtarget', 'RV', 'KV', 'CRM', 'SMM', 'MRM(IV)', 'LoC', 'SUCC']

    for target, v in results.items():
        for subtarget, vv in v.items():
            target_dir = os.path.join(BUILD, vv['hash'])
            revision = find_openwrt_revision(target_dir, '{}-{}'.format(target, subtarget))
            version = find_kernel_version(target_dir)
            crm, smm, mrm, iv = find_hardware_models(target_dir)
            loc = find_loc(target_dir)
            validation = find_validation(target_dir)
            line = [target, subtarget, revision, version, crm, smm,
                    '{}({})'.format(mrm, iv), loc, validation]
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

    args = parser.parse_args()
    offline(args)
