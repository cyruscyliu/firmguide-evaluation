#!/usr/bin/python
import json


target_board_properties = {}

with open('insights/supp_range_subtarget') as f:
    for line in f:
        # target, subtarget, type, openwrt_ver,
        #    0        1        2        3
        # kernel_ver, arch, endian, board, dt
        #     4         5      6      7     8
        if line.find('+') != -1:
            continue
        items = line.split('|')
        if items[1 + 2].strip() != 'LATEST':
            continue
        target = items[1 + 0].strip()
        subtarget = items[1 + 1].strip()
        arch = items[1 + 5].strip()
        board = items[1 + 7].split()[-1].strip()
        dt = True if items[1 + 8].strip() == 'Has DT' else False
        revision = items[1 + 3].strip()
        version = items[1 + 4].strip()

        if target not in target_board_properties:
            target_board_properties[target] = {'subtarget': []}

        target_board_properties[target]['subtarget'].append(subtarget)
        target_board_properties[target]['board'] = board
        target_board_properties[target]['arch'] = arch
        target_board_properties[target]['dt'] = dt
        target_board_properties[target]['revision'] = revision
        target_board_properties[target]['version'] = version

with open('target-board-properties.json', 'w') as f:
    json.dump(target_board_properties, f, indent=4, sort_keys=True)
