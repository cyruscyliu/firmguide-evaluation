#!/usr/bin/python
import os
import yaml
import argparse

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.compatible import find_compatible_in_fdt


BUILD = '/root/build-latest'


summary = {}


def check_version(target, subtarget, target_dir):
    image_list = yaml.safe_load(open('commandb/{}_{}.yaml'.format(target, subtarget)))
    for k, v in image_list.items():
        if not v['user_space']:
            continue
        summary['{}/{}'.format(target, subtarget)]['version'].append(v['version'])

    summary['{}/{}'.format(target, subtarget)]['version'] = \
            list(set(summary['{}/{}'.format(target, subtarget)]['version']))

def check_compatible(target, subtarget, target_dir):
    image_list = yaml.safe_load(open('commandb/{}_{}.yaml'.format(target, subtarget)))
    for k, v in image_list.items():
        if not v['user_space']:
            continue
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        path_to_dtb = profile['components']['path_to_dtb']
        if not os.path.exists(path_to_dtb):
            continue
        dts = load_dtb(path_to_dtb)
        compatible = find_compatible_in_fdt(dts)
        summary['{}/{}'.format(target, subtarget)]['machines'].extend(compatible)

    summary['{}/{}'.format(target, subtarget)]['machines'] = \
            list(set(summary['{}/{}'.format(target, subtarget)]['machines']))
        

def online_robustness(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    for target, v in results.items():
        for subtarget, vv in v.items():
            target_dir = os.path.join(BUILD, vv['hash'])
            summary['{}/{}'.format(target, subtarget)] = {'version': [], 'machines': []}
            check_version(target, subtarget, target_dir)
            check_compatible(target, subtarget, target_dir)
    for k, v in summary.items():
        print('{}@{}@{}'.format(k, v['version'], v['machines']))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)

    args = parser.parse_args()
    online_robustness(args)
