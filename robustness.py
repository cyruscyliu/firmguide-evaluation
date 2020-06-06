#!/usr/bin/python
import yaml
import argparse
from prettytable import PrettyTable


BUILD = '/root/build-latest'


arch = {}
version = {}
ftype = {}
size = {}


def check_arch(target, subtarget):
    image_list = yaml.safe_load(open('commandb/{}_{}.yaml'.format(target, subtarget)))
    for k, v in image_list.items():
        if v['arch'] not in arch:
            arch[v['arch']] = 1
        else:
            arch[v['arch']] += 1


def check_version(target, subtarget):
    image_list = yaml.safe_load(open('commandb/{}_{}.yaml'.format(target, subtarget)))
    for k, v in image_list.items():
        if v['version'] not in version:
            version[v['version']] = 1
        else:
            version[v['version']] += 1


def check_ftype(target, subtarget):
    image_list = yaml.safe_load(open('commandb/{}_{}.yaml'.format(target, subtarget)))
    for k, v in image_list.items():
        if v['type'] not in ftype:
            ftype[v['type']] = 1
        else:
            ftype[v['type']] += 1


def check_size(target, subtarget):
    image_list = yaml.safe_load(open('commandb/{}_{}.yaml'.format(target, subtarget)))
    for k, v in image_list.items():
        if v['size'] not in size:
            size[v['size']] = 1
        else:
            size[v['size']] += 1


def online_robustness(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    for target, v in results.items():
        for subtarget, vv in v.items():
            check_arch(target, subtarget)
            check_version(target, subtarget)
            check_ftype(target, subtarget)
            check_size(target, subtarget)

    # #### ARCH&ENDIAN
    table_arch = PrettyTable()
    table_arch.field_names = ['ARCH&ENDIAN', 'COUNT']
    for k, v in arch.items():
        table_arch.add_row([k, v])
    with open('online-robustness.arch.csv', 'w') as f:
        f.write(table_arch.get_csv_string())
    print('save as online-robustness.arch.csv')

    # #### TYPE
    table_type = PrettyTable()
    table_type.field_names = ['TYPE', 'COUNT']
    for k, v in ftype.items():
        table_type.add_row([k, v])
    with open('online-robustness.type.csv', 'w') as f:
        f.write(table_type.get_csv_string())
    print('save as online-robustness.type.csv')

    # #### SIZE
    table_size = PrettyTable()
    table_size.field_names = ['SIZE', 'COUNT']
    for k, v in size.items():
        table_size.add_row([k, v])
    with open('online-robustness.size.csv', 'w') as f:
        f.write(table_size.get_csv_string())
    print('save as online-robustness.size.csv')

    # #### VERSION
    table_version = PrettyTable()
    table_version.field_names = ['VERSION', 'COUNT']
    for k, v in version.items():
        table_version.add_row([k, v])
    with open('online-robustness.version.csv', 'w') as f:
        f.write(table_version.get_csv_string())
    print('save as online-robustness.version.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)

    args = parser.parse_args()
    online_robustness(args)
