#!/usr/bin/python
import sys
import random


def sample(path_to_commands):
    """We will sample 100 commands in given commands."""
    commands = []
    with open(path_to_commands) as f:
        commands = f.readlines()
    if len(commands) > 100:
        commands = random.sample(commands, 100)
    new_path_to_commands = path_to_commands[:-2] + '100.sh'
    with open(new_path_to_commands, 'w') as f:
        f.writelines(commands)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path_to_commands = sys.argv[1]
    else:
        print('usage: {} path/to/commands'.format(sys.argv[0]))
        exit()
    sample(path_to_commands)

