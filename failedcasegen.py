#!/usr/bin/python
import os
import yaml
import argparse


def load_all_commands():
    with open('commandb.sh') as f:
        commands = f.readlines()
    return commands


def search_command(commands, key):
    for command in commands:
        if command.find(key) != -1:
            return command
    return None


def failedcasegen(summaryp, args):
    commands = load_all_commands()
    failed_commands = []

    summary = yaml.safe_load(open(summaryp))
    for k, v in summary.items():
        if not v['format']:
            continue
        if not v['kernel_extracted']:
            continue
        if not v['match']:
            continue
        if not v['prepare']:
            continue
        if 'failed_rootfs' in v:
            continue
        if 'failed_shell' in v:
            continue
        if not v['rootfs']:
            if not v['user_space'] and v['shell']:
                print('>>>> ERRROR <<<< invalid {}'.format(k))
                continue
            elif v['user_space']:
                print('>>>> ERRROR <<<< invalid {}'.format(k))
                continue
        elif v['rootfs'] and not['user_space'] and v['shell']:
                print('>>>> ERRROR <<<< invalid {}'.format(k))
                continue
        assert v['prepare'], 'all is prepared'

        if args.rootfs:
            if v['rootfs']:
                continue
        elif args.user_space:
            if v['user_space']:
                continue
        elif args.shell:
            if v['shell']:
                continue

        command = search_command(commands, k)
        if command is None:
            print('>>>> ERRROR <<<< there is no command for {}'.format(k))
            continue
        failed_commands.append(command)

    if args.rootfs:
        indicator = 'not_rootfs'
    elif args.user_space:
        indicator = 'not_user_level'
    elif args.shell:
        indicator = 'not_shell'

    path = os.path.join(os.path.dirname(summaryp),
            os.path.basename(summaryp).split('.')[0] + '.' + indicator)
    with open(path, 'w') as f:
        for command in failed_commands:
            f.write(command)
    print('save as {}'.format(path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('imagelist')
    parser.add_argument('-r', '--rootfs', action='store_true', default=False)
    parser.add_argument('-u', '--user_space', action='store_true', default=False)
    parser.add_argument('-s', '--shell', action='store_true', default=False)
    args = parser.parse_args()
    summary = args.imagelist
    shell = args.shell

    failedcasegen(summary, args)
