#!/usr/bin/python3
"""
This script collects all evaluation results and provides a user friendly
interface.
"""
import argparse


def image_statistics(args):
    print('== image statistics')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help='sub-command help')
    stats = subparsers.add_parser('stats', help='image statistics')
    stats.set_defaults(func=image_statistics)

    args = parser.parse_args()
    args.func(args)
