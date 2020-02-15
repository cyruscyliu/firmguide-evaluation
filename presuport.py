#!/usr/bin/python
import yaml

support = {'arm': {}, 'mips':{}}

# mach-dir
## machine_ids
## compatible
## profiles
### path, kernel_version, brand, brand_revision, cmdline, nvram
## device_tree

## load the latest one
dtd = yaml.safe_load(open('insights/support.arm.yaml'))
support['arm'] = dtd
dtd = yaml.safe_load(open('insights/support.mips.yaml'))
support['mips'] = dtd

# update openwrt target/kernel board mapping
with open('insights/latest_target') as f:
    for line in f:
        # ['zynq', '=>', '☑', 'mach-zynq', '(openwrt-19.07.0', '4.14', 'arm)', '"1', 'sub', 'releases"']
        #    0            2                        4                     6
        things = line.strip().split()
        target = things[0]
        mach = things[3]
        arch = things[6].strip(')')
        if mach not in support[arch]:
            support[arch][mach] = {
                'machine_ids': {},
                'compatible': {},
                'profiles': {},
                'device_tree': None,
                'targets': {}
            }
            support[arch][mach]['targets']['openwrt'] = [target]
        else:
            if 'targets' not in support[arch][mach]:
                support[arch][mach]['targets'] = {'openwrt':[]}
            support[arch][mach]['targets']['openwrt'].append(target)

yaml.safe_dump(support['arm'], open('support.arm.yaml', 'w'))
yaml.safe_dump(support['mips'], open('support.mips.yaml', 'w'))


