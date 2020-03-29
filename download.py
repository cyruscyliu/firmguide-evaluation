#!/usr/bin/python
import os

with open('download.sh') as f:
    for line in f:
        local_path = line.strip().split()[-1]
        if os.path.exists(local_path):
            continue
        print(line.strip())
