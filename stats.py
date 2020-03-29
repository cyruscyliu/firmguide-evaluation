#!/usr/bin/python
import os
import sys
import yaml
from prettytable import PrettyTable


WORKING_DIR = '/root/build'

pt = PrettyTable(['uuid', 'unpacked', 'has_kernel', 'user_level'])

rows = {}
summary = {}


def stats(argv):
    for uuid in os.listdir(WORKING_DIR):
        if uuid in ['qemu-4.0.0', 'binwalk-2.1.1']:
            continue
        if uuid.startswith('buildroot'):
            continue
        commands_not_user_level = []
        commands_user_level = []
        commands_no_kernel = []
        rows[uuid] = {}
        summary[uuid] = {'unpacked': 0, 'user_level': 0, 'has_kernel': 0}

        path_to_uuid = os.path.join(WORKING_DIR, uuid)
        if os.path.isfile(path_to_uuid):
            continue

        for profile in os.listdir(path_to_uuid):
            if profile == 'profile.yaml':
                continue
            if not profile.endswith('profile.yaml'):
                continue
            fn = profile.split('.profile.yaml')[0]
            try:
                int(fn[:-4], 16)
            except ValueError:
                continue

            path_to_profile = os.path.join(path_to_uuid, profile)

            rows[uuid][fn] = {}
            path_to_stats = os.path.join(path_to_uuid, '{}.stats.yaml'.format(fn))
            if not os.path.exists(path_to_stats):
                rows[uuid][fn]['unpacked'] = False
                rows[uuid][fn]['has_kernel'] = False
                rows[uuid][fn]['user_level'] = False
                profile_json = yaml.safe_load(open(path_to_profile))
                print(fn, '\n    ', profile_json['brand']['url'])
                continue

            rows[uuid][fn]['unpacked'] = True
            summary[uuid]['unpacked'] += 1

            stats = yaml.safe_load(open(path_to_stats))
            if stats['components']['path_to_kernel'] is False:
                rows[uuid][fn]['has_kernel'] = False
                rows[uuid][fn]['user_level'] = False
                commands_no_kernel.extend(os.popen('grep {} commandb.sh'.format(fn)).readlines())
                continue

            rows[uuid][fn]['has_kernel'] = True
            summary[uuid]['has_kernel'] += 1

            if isinstance(stats['runtime'], dict) and stats['runtime']['user_mode']:
                rows[uuid][fn]['user_level'] = True
                summary[uuid]['user_level'] += 1
                commands_user_level.extend(os.popen('grep {} commandb.sh'.format(fn)).readlines())
            else:
                rows[uuid][fn]['user_level'] = False
                commands_not_user_level.extend(os.popen('grep {} commandb.sh'.format(fn)).readlines())

        with open('commandb/{}.no_kernel'.format(uuid), 'w') as f:
            f.write(''.join(commands_no_kernel))
        with open('commandb/{}.not_user_level'.format(uuid), 'w') as f:
            f.write(''.join(commands_not_user_level))
        with open('commandb/{}.user_level'.format(uuid), 'w') as f:
            f.write(''.join(commands_user_level))
        if len(rows[uuid]) == 0:
            continue
        # summary
        pt.add_row([
            uuid,
            '{:.2f}% ({}/{})'.format(summary[uuid]['unpacked']/len(rows[uuid])*100, summary[uuid]['unpacked'], len(rows[uuid])),
            '{:.2f}% ({}/{})'.format(summary[uuid]['has_kernel']/len(rows[uuid])*100, summary[uuid]['has_kernel'], len(rows[uuid])),
            '{:.2f}% ({}/{})'.format(summary[uuid]['user_level']/len(rows[uuid])*100, summary[uuid]['user_level'], len(rows[uuid])),
        ])

    if len(argv) == 2 and argv[1] == '-j':
        print(pt.get_json_string())
    else:
        print(pt)

if __name__ == '__main__':
    stats(sys.argv)

