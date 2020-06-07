#!/usr/bin/python
import os
import sys

def envgen(cmdlinef, name):
    """
    /root/build-latest/qemu-4.0.0/mipsel-softmmu/qemu-system-mipsel \ # 0
            -M ralink_rt3050_soc \                                    # 1, 2
            -kernel ////.bin.extracted/0.uimage \                     # 3, 4
            -dtb //////ralink_rt3050_soc.dtb,offset=0x410 \           # 5, 6
            -nographic \                                              # 7
            -initrd /root/esv-latest/rootfs/mipsel.cpio.rootfs \      # 8, 9
            -append "console=ttyS0 nowatchdog nokaslr" \
            -chardev stdio,mux=on,id=char0 \
            -mon chardev=char0,mode=readline \
            -serial chardev:char0 -serial chardev:char0
    """
    with open(cmdlinef) as f:
        cmdline = f.readline()
    items = cmdline.split()

    # prepare 
    os.makedirs(name, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(name)
    # copy qemu-system-archendian
    os.system('cp {} .'.format(items[0]))
    items[0] = os.path.basename(items[0])
    # copy kernel
    os.system('cp {} .'.format(items[4]))
    items[4] = os.path.basename(items[4])
    # copy dtb
    dtb_items = items[6].split(',')
    os.system('cp {} .'.format(dtb_items[0]))
    dtb_items[0] = os.path.basename(dtb_items[0])
    items[6] = ','.join(dtb_items)
    # copy rootfs
    os.system('cp {} .'.format(items[9]))
    items[9] = os.path.basename(items[9])

    with open('boot.sh', 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('./{}'.format(items[0]))
        for item in items[1:]:
            if item.startswith('-'):
                f.write(' \\\n\t{}'.format(item))
            else:
                f.write(' {}'.format(item))

    os.system('chmod +x boot.sh')
    os.chdir(cwd)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python {} cmdlinef name'.format(sys.argv[0]))
        exit(-1)

    cmdlinef = sys.argv[1]
    name = sys.argv[2]
    envgen(cmdlinef, name)
