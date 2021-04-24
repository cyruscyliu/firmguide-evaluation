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

soc_dict = {
    'plxtech,nas7820': 'plx nas7820',
    'marvell,kirkwood-88f6282': 'marvell 88f6282',
    'marvell,kirkwood-88f6281': 'marvell 88f6281',
    'marvell,kirkwood-88f6192': 'marvell 88f6192',
    'brcm,bcm4709': 'Broadcom BCM4709A0',
    'brcm,bcm4708': 'Broadcom BCM4708A0',
    'brcm,bcm47189': 'Broadcom BCM47189',
    'qca,qca9342': 'Qualcomm Atheros QCA9342',
    'qca,qca9344': 'Qualcomm Atheros QCA9344',
    'qca,qca9531': 'Qualcomm Atheros QCA9531',
    'qca,qca9533': 'Qualcomm Atheros QCA9533',
    'qca,qca9557': 'Qualcomm Atheros QCA9557',
    'qca,qca9558': 'Qualcomm Atheros QCA9558',
    'qca,qca9560': 'Qualcomm Atheros QCA9560',
    'qca,qca9561': 'Qualcomm Atheros QCA9561',
    'qca,qca9563': 'Qualcomm Atheros QCA9563',
    'qca,ar9330': 'Atheros AR9330',
    'qca,ar9331': 'Atheros AR9331',
    'qca,ar9341': 'Atheros AR9341',
    'qca,ar9342': 'Atheros AR9342',
    'qca,ar9344': 'Atheros AR9344',
    'qca,ar7161': 'Atheros AR7161',
    'qca,ar7241': 'Atheros AR7241',
    'qca,ar7242': 'Atheros AR7242',
    'ralink,rt3050-soc': 'Ralink RT3050',
    'ralink,rt3052-soc': 'Ralink RT3052',
    'ralink,rt3352-soc': 'Ralink RT3352',
    'ralink,rt5350-soc': 'Ralink RT5350',
}

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
            summary[soc] = {}
            soc_c += 1
            print('== possible soc {} in {}'.format(soc, compatible))
        if 'images' not in summary[soc]:
            summary[soc]['images'] = {}
        summary[soc]['images'][k] = v
        summary[soc]['target_dir'] = target_dir
    print('[-] Skip {} images'.format(skipped))
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
    with open('soc-latest-statistics.yaml', 'w') as f:
        yaml.safe_dump(summary, f)
    print('[-] soc statistics saved as soc-latest-statistics.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-j', '--json', help='Generate JSON data.', action='store_true', default=False)
    parser.add_argument('-c', '--csv', help='Generate CSV data.', action='store_true', default=False)
    parser.add_argument('-s', '--select', help='Assign a particular target/subtarget, such as oxnas/generic.')

    args = parser.parse_args()
    soc(args)
