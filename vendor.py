#!/usr/bin/python
import os
import yaml
import datetime
import argparse

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.compatible import find_model_in_fdt
from slcore.dt_parsers.intc import find_flatten_intc_in_fdt
from slcore.dt_parsers.timer import find_flatten_timer_in_fdt
from prettytable import PrettyTable
from online import gen_image_list


BUILD = '/root/build-latest'

brand_dict = {
    'mitrastar': 'mitrastar technology corp.',
    'i-o': 'i-o data',
    'cloud': 'cloud engines',
    'western': 'western digital',
    'embedded': 'embedded wireless',
    'wr512-3gn': 'evaluation board',
    'a5-v11': 'evaluation board',
    'wr512-3gn-like': 'evaluation board',
    'senao': 'engenius',
    'vocore': 'vocore',
    'rt5350f-olinuxino': 'olimex',
}

summary = {}

def vendor_statistics(target_dir, image_list):
    skipped = 0
    brand_c = 0
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        path_to_dtb = profile['components']['path_to_dtb']
        if path_to_dtb is None:
            skipped += 1
            continue
        dts = load_dtb(path_to_dtb)
        model = find_model_in_fdt(dts)
        assert len(model) == 1, 'model is {}'.format(model)
        model = model[0]
        items = model.split()
        brand = items[0].lower()
        if len(items) == 1:
            if brand in brand_dict:
                brand = brand_dict[brand]
            else:
                print('[-] unknown {}'.format(model))
                skipped += 1
                continue
        else:
            if brand in brand_dict:
                brand = brand_dict[brand]
        if brand not in summary:
            summary[brand] = {}
            brand_c += 1
            print('== possible brand {} in {}'.format(brand, model))
        if 'images' not in summary[brand]:
            summary[brand]['images'] = {}
        summary[brand]['images'][k] = v
        summary[brand]['target_dir'] = target_dir
    print('[-] Skip {} images'.format(skipped))
    print('[+] Found {} brands'.format(brand_c))
    return skipped


def vendor(argv):
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
            vendor_statistics(target_dir, image_list)
    with open('vendor-statistics.yaml', 'w') as f:
        yaml.safe_dump(summary, f)
    print('[-] vendor statistics saved as vendor-statistics.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)
    parser.add_argument('-s', '--select', help='Assign a particular target/subtarget, such as oxnas/generic.')

    args = parser.parse_args()
    vendor(args)
