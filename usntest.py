import os

from slcore.dt_parsers.common import load_dtb
from slcore.dt_parsers.serial import find_flatten_serial_in_fdt
from slcore.dt_parsers.intc import find_flatten_intc_in_fdt
from slcore.dt_parsers.cpu import find_flatten_cpu_in_fdt
from slcore.brick import Brick


def usntest_run(path_to_dtb):
    dts = load_dtb(path_to_dtb)

    # test serial model
    s_supported = False
    serials = find_flatten_serial_in_fdt(dts)
    if serials is not None:
        for serial in serials:
            b = Brick('serial', serial['compatible'])
            if b.supported:
                s_supported = True

    # test smp
    s_smp = False
    cpus = find_flatten_cpu_in_fdt(dts)
    if cpus is not None:
        if len(cpus) == 1:
            return s_supported, s_smp, None
        else:
            s_smp = True

    # test intc model
    s_intc = False
    intcs = find_flatten_intc_in_fdt(dts)
    if intcs is not None:
        for intc in intcs:
            b = Brick('intc', intc['compatible'])
            if b.supported:
                s_intc = True

    return s_supported, s_smp, s_intc
