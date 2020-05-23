#!/usr/bin/python
import yaml
import argparse

from elftools.elf.elffile import ELFFile
from frequency import parse_openwrt_url

OBD = '/mnt/iscsi/openwrt-build-docker'
BUILD = '~/build'


def find_arch_and_endian(path_to_vmlinux):
    elffile = ELFFile(open(path_to_vmlinux, 'rb'))
    arch = elffile.get_machine_arch().lower()
    endian = 'l' if elffile.little_endian else 'b'
    return arch, endian


def find_target_and_subtarget(image_builder_hash):
    cache_image_builder_table = {}
    with open('{}/image_builder.cache'.format(OBD)) as f:
        for line in f:
            things = line.strip().split(',')
            cache_image_builder_table[things[0]] = things[2]

    if image_builder_hash in cache_image_builder_table:
        _, target, subtarget = parse_openwrt_url(
            cache_image_builder_table[image_builder_hash])
        return target, subtarget

    return None, None


def generate_commands(args):
    support_list = yaml.safe_load(
        open('{}/summary.yaml'.format(OBD)))
    for k, v in support_list.items():
        arch, endian = find_arch_and_endian('{}/{}'.format(OBD, v['path_to_vmlinux']))
        target, subtarget = find_target_and_subtarget(k)
        if target is None:
            continue
        command = ['./salamander', 'create']
        command.append('-n {}-{}-{}'.format(v['revision'], target, subtarget))
        command.append('-a {}'.format(arch))
        command.append('-e {}'.format(endian))
        command.append('-p {}/{}'.format(BUILD, k))
        command.append('-b {}'.format('openwrt'))
        command.append('-t {}'.format(target))
        command.append('-st {}'.format(subtarget))
        command.append('-s {}/{}'.format(OBD, v['path_to_source_code']))
        command.append('-cc {}/{}'.format(OBD, v['path_to_gcc'][:-3]))
        command.append('-m {}/{}'.format(OBD, v['path_to_makeout']))
        print(' '.join(command))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    args = parser.parse_args()
    generate_commands(args)
