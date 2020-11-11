#!/usr/bin/python
import os
import yaml

from prettytable import PrettyTable
from online import find_format, find_kernel_extracted, find_match, \
        find_prepare, find_rootfs, find_user_space, find_shell, \
        find_time, gen_image_list


peripheral_model_intcs = []
peripheral_model_timers = []
summary_number_of_soc = {'intc': {}, 'timer': {}}


def list_all_peripheral_models():
    global peripheral_model_intcs
    global peripheral_model_timers
    soc_statistics = yaml.safe_load(open('soc-statistics.yaml'))
    for _, statistics in soc_statistics.items():
        peripheral_model_intcs.extend(statistics['intc'])
        peripheral_model_timers.extend(statistics['timer'])
    peripheral_model_intcs = list(set(peripheral_model_intcs))
    peripheral_model_timers = list(set(peripheral_model_timers))
    print('[001]  intc: {}'.format(peripheral_model_intcs))
    print('[001] timer: {}'.format(peripheral_model_timers))

    for intc in peripheral_model_intcs:
        if intc.find('gpio') != -1:
            continue
        if intc.find('pci') != -1:
            continue
        summary_number_of_soc['intc'][intc] = {'number_of_soc': 0}
    for timer in peripheral_model_timers:
        summary_number_of_soc['timer'][timer] = {'number_of_soc': 0}
    print('[002] soc: {}'.format(len(soc_statistics)))


def first_number_of_soc():
    soc_statistics = yaml.safe_load(open('soc-statistics.yaml'))
    for _, statistics in soc_statistics.items():
        intcs = list(set(statistics['intc']))
        for intc in intcs:
            if intc in summary_number_of_soc['intc']:
                summary_number_of_soc['intc'][intc]['number_of_soc'] += 1
        timers = list(set(statistics['timer']))
        for timer in timers:
            if timer in summary_number_of_soc['timer']:
                summary_number_of_soc['timer'][timer]['number_of_soc'] += 1
    with open('soc-reevaluation.yaml', 'w') as f:
        yaml.safe_dump(summary_number_of_soc, f)
    print('[-] soc summary saved as soc-reevaluation.yaml')


def second_success_rate_of_soc():
    table = PrettyTable()
    table.field_names = [
        'SOC', 'SUM',
        'FORMAT', 'KERNEL_EXTRACTED',
        'ROOTFS', 'USER_SPACE', 'SHELL', 'TIME'
    ]
    soc_statistics = yaml.safe_load(open('soc-statistics.yaml'))
    for soc, statistics in soc_statistics.items():
        image_list = statistics['images']
        target_dir = statistics['target_dir']
        unpack_format = find_format(target_dir, image_list)
        unpack_kernel_extracted = \
            find_kernel_extracted(target_dir, image_list)
        match = find_match(target_dir, image_list)
        prepare = find_prepare(target_dir, image_list)
        boot_rootfs, failed_rootfs = find_rootfs(target_dir, image_list)
        boot_user_space = find_user_space(target_dir, image_list)
        boot_shell, failed_shell = find_shell(target_dir, image_list)
        time = find_time(target_dir, image_list)
        line = [soc.replace(',', '#'), len(image_list), unpack_format, unpack_kernel_extracted,
                '{}({})'.format(boot_rootfs, failed_rootfs),
                boot_user_space, '{}({})'.format(boot_shell, failed_shell),
                '{:.2f}'.format(time)]
        table.add_row(line)
    print(table.get_csv_string())


if __name__ == '__main__':
    if not os.path.exists('soc-statistics.yaml'):
        print('[-] error: please run ./soc.py first')
        exit()
    list_all_peripheral_models()
    # first_number_of_soc()
    second_success_rate_of_soc()
