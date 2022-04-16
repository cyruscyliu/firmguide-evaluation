#!/usr/bin/python
import csv

words = {
    '10.03': ['backfire'],
    '12.09': ['attitude', 'adjustment'],
    '14.07': ['barrier', 'breaker'],
    '15.05': ['chaos', 'calmer'],
    '17.01.x': ['lede']
}


stats = {
    '10.03': 0,
    '12.09': 0,
    '14.07': 0,
    '15.05': 0,
    '17.01.x': 0,
}


def parse_shodan_openwrt():
    with open('shodan-export.csv') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            banner = row[2]
            if banner == 'Banner':
                continue
            banner = banner.lower()
            banner = banner.strip().replace('/', '@#').replace('\n', '@#').replace(':', '@#').replace('_', '@#').replace('__', '@#').replace(' ', '@#')
            tokens = banner.split('@#')
            for token in tokens:
                for k, v in words.items():
                    if token in v:
                        stats[k] += 1
                        break
    print(stats)

if __name__ == '__main__':
    parse_shodan_openwrt()

