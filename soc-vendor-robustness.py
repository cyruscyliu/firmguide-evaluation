#!/usr/bin/python3
import yaml

soc = yaml.safe_load(open('soc-latest-statistics.yaml'))
print('soc,count')
for k, v in soc.items():
    print('{},{}'.format(k, len(v['images'])))
vendor = yaml.safe_load(open('vendor-statistics.yaml'))
print('vendor,count')
for k, v in vendor.items():
    print('{},{}'.format(k, len(v['images'])))
