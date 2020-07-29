#!/usr/bin/python
import os
import yaml
import datetime
import argparse

from prettytable import PrettyTable
from offline import find_kernel_version2


BUILD = '/root/build-latest'


def find_arch(target_dir, image_list):
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        image_list[k]['arch'] = profile['basics']['architecture'] + 'e' + profile['basics']['endian']
        now = ' '.join(line.split()[:2])
        try:
            now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S,%f')
        except ValueError:
            continue


def find_size(target_dir, image_list):
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        image_list[k]['size'] = os.path.getsize(profile['components']['path_to_raw'])


def find_version(target_dir, image_list):
    print('>>>>>>>> FIND KERNEL VERSION ...')
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        version = None
        if 'path_to_kernel' in profile['components']:
            path_to_kernel = profile['components']['path_to_kernel']
            try:
                version = find_kernel_version2(path_to_kernel)
            except FileNotFoundError:
                pass
        image_list[k]['version'] = version


def find_type(target_dir, image_list):
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        image_list[k]['type'] = profile['components']['type']


def find_format(target_dir, image_list):
    c = 0
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        if profile['components']['supported']:
            c += 1
            image_list[k]['format'] = True
        else:
            image_list[k]['format'] = False
    return c


def find_kernel_extracted(target_dir, image_list):
    c = 0
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        if profile['components']['path_to_kernel'] is not None:
            c += 1
            image_list[k]['kernel_extracted'] = True
        else:
            image_list[k]['kernel_extracted'] = False
    return c


def find_match(target_dir, image_list):
    c = 0
    for k, v in image_list.items():
        log = os.path.join(target_dir, v['log'])
        status = 0
        with open(log) as f:
            for line in f:
                if line.find('components is missing') != -1:
                    status = -1
                if line.find('firmware format is not supported') != -1:
                    status = -1
                if line.find('firmware have no kernel, maybe is a rootfs image') != -1:
                    status = -1
                if line.find('001 cannot find the board') != -1:
                    status = -1
                if line.find('002 cannot find the compatible') != -1:
                    status = -1
                if line.find('003 cannot find any machine id') != -1:
                    status = -1
        if status == 0:
            c += 1
            image_list[k]['match'] = True
        else:
            image_list[k]['match'] = False
            if image_list[k]['kernel_extracted']:
                image_list[k]['match'] = True
    return c


def find_prepare(target_dir, image_list):
    c = 0
    for k, v in image_list.items():
        log = os.path.join(target_dir, v['log'])
        status = 0
        with open(log) as f:
            for line in f:
                if line.find('repack kernel') != -1:
                    status += 1
                if line.find('get command') != -1:
                    status += 1
        if status == 2:
            c += 1
            image_list[k]['prepare'] = True
        else:
            image_list[k]['prepare'] = False
    return c


def find_rootfs(target_dir, image_list):
    c, c1 = 0, 0

    for k, v in image_list.items():
        log = os.path.join(target_dir, v['log'])
        status = 0
        reason = None
        output = False
        counter = 0
        with open(log) as f:
            for line in f:
                if line.find('Unpacking initramfs') != -1:
                    status += 1
                elif line.find('Unable to mount root fs on unknown-block(0,0)') != -1:
                    reason = 'flag_unset'
                elif line.find('CPU clock: 0.000 MHz') != -1:
                    reason = 'zero_rate'
                elif line.find('Data bus error') != -1:
                    reason = 'data_bus_error'
                elif line.find('Failed to get CPU node') != -1:
                    reason = 'failed_cpu_node'
                elif line.find('Failed to find ralink,rt3050-sysc node') != -1:
                    reason = 'failed_sysc_node'
                if line.find('tracing - [') != -1:
                    output = True
                if line.find('SoC Type: Ralink RT3052 id:0 rev:0') != -1:
                    counter += 1
        if status == 1:
            c += 1
            image_list[k]['rootfs'] = True
        else:
            if reason is not None:
                image_list[k]['failed_rootfs'] = reason
                c1 += 1
            elif not output and image_list[k]['prepare']:
                image_list[k]['failed_rootfs'] = 'no_output'
                print(k)
                c1 += 1
            elif counter > 1:
                image_list[k]['failed_rootfs'] = 'repeating'
                c1 += 1
            image_list[k]['rootfs'] = False
    return c, c1


def find_user_space(target_dir, image_list):
    c = 0
    for k, v in image_list.items():
        profile = yaml.safe_load(open(os.path.join(target_dir, v['profile'])))
        if profile['runtime']['user_mode']:
            c += 1
            image_list[k]['user_space'] = True
        else:
            image_list[k]['user_space'] = False
    return c


def find_shell(target_dir, image_list):
    c, c1 = 0, 0
    for k, v in image_list.items():
        log = os.path.join(target_dir, v['log'])
        status = 0
        reason = None
        with open(log) as f:
            for line in f:
                if line.find('Starting syslogd') != -1:
                    status += 1
                if line.find('Welcome to Buildroot') != -1:
                    status += 1
                if line.find('Unhandled fault: page domain fault (0x81b) at 0x00000200') != -1:
                    status = 0
                    reason = 'orion_nand_bug'
                if line.find('platform pinctrl: function \'uartlite\' not supported') != -1:
                    status = 0
                    reason = 'serial_failure'
                if line.find('Unable to handle kernel NULL pointer dereference at virtual address 00000200') != -1:
                    print('orion_nand_bug found which should be in the find_user_space')
                    status = 0
        if status > 0:
            c += 1
            image_list[k]['shell'] = True
            if not image_list[k]['user_space']:
                print(k)
        else:
            if reason is not None:
                image_list[k]['failed_shell'] = reason
                c1 += 1
            image_list[k]['shell'] = False
    return c, c1


def find_time(target_dir, image_list):
    t = 0
    c = 0
    for k, v in image_list.items():
        log = os.path.join(target_dir, v['log'])
        start, end = None, None
        with open(log) as f:
            for line in f:
                if line.find('- msearch -') != -1:
                    start = ' '.join(line.split()[:2])
                    start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S,%f')
                if line.find('snapshot - source at') != -1:
                    end = ' '.join(line.split()[:2])
                    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S,%f')
        if start is not None and end is not None:
            if v['user_space']:
                t += (end.timestamp() - start.timestamp())
                c += 1
                image_list[k]['time'] = t
    if c == 0:
        return .0
    else:
        return t / c


def gen_image_list(target, subtarget, target_dir):
    image_list = {}
    with open('commandb/{}_{}.sh'.format(target, subtarget)) as f:
        for line in f:
            filename = os.path.basename(line.split()[6])
            if not os.path.exists(os.path.join(target_dir, filename)):
                continue
            profile = '{}.profile.yaml'.format(filename)
            log = '{}.log'.format(filename)
            trace = '{}.trace'.format(filename)
            if not os.path.exists(os.path.join(target_dir, profile)):
                print('BUG: {}/{}/{} is missing'.format(target, subtarget, profile))
                continue
            image_list[filename] = {'profile': profile, 'log': log, 'trace': trace}
    return image_list


def online(argv):
    results = yaml.safe_load(open('subtarget-hashtable.yaml'))

    table = PrettyTable()
    table.field_names = [
        'TARGET', 'SUBTARGET', 'SUM', 'FORMAT', 'KERNEL_EXTRACTED', 'MATCH',
        'PREPARE', 'ROOTFS', 'USER_SPACE', 'SHELL', 'TIME'
    ]

    for target, v in results.items():
        for subtarget, vv in v.items():
            if argv.select is not None:
                if '{}/{}'.format(target, subtarget) != argv.select:
                    continue
            print('>>>> HANDLE {}/{}'.format(target, subtarget))
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
            line = [target, subtarget, len(image_list), unpack_format, unpack_kernel_extracted,
                    match, prepare, '{}({})'.format(boot_rootfs, failed_rootfs),
                    boot_user_space, '{}({})'.format(boot_shell, failed_shell),
                    '{:.2f}'.format(time)]
            table.add_row(line)
            find_size(target_dir, image_list)
            find_type(target_dir, image_list)
            find_version(target_dir, image_list)
            find_arch(target_dir, image_list)
            yaml.safe_dump(image_list, open('commandb/{}_{}.yaml'.format(target, subtarget), 'w'))

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
