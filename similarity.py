#!/usr/bin/python
import sys


def horizontal(data):
    saved_identi = None
    summary = {}
    with open(data) as f:
        for line in f:
            if line.startswith('K1'):
                continue
            cells = line.split(',')
            if len(cells) < 2:
                continue
            if cells[0].find('/') != -1:
                identi = cells[0]
            else:
                identi = '{}/{}'.format(cells[0], cells[1])
            if identi != saved_identi:
                summary[identi] = []
                saved_identi = identi
            summary[identi].append(sum([int(i) for i in cells[3:]]))

    output = {}
    for k, v in summary.items():
        summary[k] = {'data': v, 'avg': sum(v) / len(v)}
        output[k] = summary[k]['avg']

    for k, v in output.items():
        print('{},{}'.format(k, v))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} data')
        exit(-1)

    data = sys.argv[1]
    horizontal(data)
