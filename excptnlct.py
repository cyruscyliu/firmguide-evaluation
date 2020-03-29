#!/usr/bin/python
import os
import sys

def exception_locate(commands, build):
    with open(commands) as f:
        for line in f:
            fname = os.path.basename(line.split()[6])
            profile = os.path.join(build, '{}.profile.yaml'.format(fname))
            if not os.path.exists(profile):
                print(line.strip())

if __name__ == '__main__':
    if len(sys.argv) == 3:
        commands = sys.argv[1]
        build = sys.argv[2]
    else:
        print('usage {} path/to/commands dir/to/build'.format(sys.argv[0]))
        exit()
    exception_locate(commands, build)


