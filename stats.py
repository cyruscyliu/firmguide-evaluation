#!/usr/bin/python
import os
import sys
import yaml
from prettytable import PrettyTable


WORKING_DIR = '/root/build'

pt = PrettyTable(['uuid', 'unpacked', 'user_level'])

rows = {}
summary = {}

def stats(argv):
    for uuid in os.listdir(WORKING_DIR):
        rows[uuid] = {}
        summary[uuid] = {'unpacked': 0, 'profiled': 0, 'user_level': 0}

        p = os.path.join(WORKING_DIR, uuid)
        if os.path.isfile(p):
            continue
        for profile in os.listdir(p):
            if profile == 'profile.yaml':
                continue
            if not profile.endswith('profile.yaml'):
                continue
            fn = profile.split('.profile.yaml')[0]
            rows[uuid][fn] = {}
            pp = os.path.join(p, '{}.stats.yaml'.format(fn))
            if not os.path.exists(pp):
                rows[uuid][fn]['unpacked'] = False
                rows[uuid][fn]['user_level'] = False
                print(pp)
                continue

            rows[uuid][fn]['unpacked'] = True
            summary[uuid]['unpacked'] += 1
            stats = yaml.safe_load(open(pp))
            if stats['runtime']['user_mode']:
                rows[uuid][fn]['user_level'] = True
                summary[uuid]['user_level'] += 1
            else:
                rows[uuid][fn]['user_level'] = False
        if len(rows[uuid]) == 0:
            continue
        # summary
        pt.add_row([
            uuid,
            '{:.2f}% ({}/{})'.format(summary[uuid]['unpacked']/len(rows[uuid])*100, summary[uuid]['unpacked'], len(rows[uuid])),
            '{:.2f}% ({}/{})'.format(summary[uuid]['user_level']/len(rows[uuid])*100, summary[uuid]['user_level'], len(rows[uuid])),
        ])

    if len(argv) == 2 and argv[1] == '-j':
        print(pt.get_json_string())
    else:
        print(pt)

if __name__ == '__main__':
    stats(sys.argv)

