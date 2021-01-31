#!/usr/bin/python
import os
import yaml


def real_soc_stats(pathname):
    if not os.path.exists(pathname):
        print('Please generated {} first'.format(pathname))
        exit(-1)

    real_socs = {}

    results = yaml.safe_load(open(pathname))
    for key in results.keys():
        real_soc = key.split('@')[-1]
        if real_soc in real_socs:
            real_socs[real_soc] += 1
        else:
            real_socs[real_soc] = 1

    for k, v in real_socs.items():
        print(k, v)

if __name__ == '__main__':
    real_soc_stats('soc-statistics.yaml')
