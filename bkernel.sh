#!/bin/sh

test_whetstone()
{
    #
    # Loops: 1000, Iterations: 1, Duration: 172 sec.
    # C Converted Double Precision Whetstones: 581.4 KIPS
    whetstone
}

test_dhrystone()
{
    #
    # Dhrystone Benchmark, Version 2.1 (Language: C)
    #
    # Program compiled without 'register' attribute
    #
    # Execution starts, 1000000 runs through Dhrystone
    # Execution ends
    #
    # Final values of the variables used in the benchmark:
    #
    # Int_Glob:            5
    #         should be:   5
    # Bool_Glob:           1
    #         should be:   1
    # Ch_1_Glob:           A
    #         should be:   A
    # Ch_2_Glob:           B
    #         should be:   B
    # Arr_1_Glob[8]:       7
    #         should be:   7
    # Arr_2_Glob[8][7]:    1000010
    #         should be:   Number_Of_Runs + 10
    # Ptr_Glob->
    #   Ptr_Comp:          24027536
    #         should be:   (implementation-dependent)
    #   Discr:             0
    #         should be:   0
    #   Enum_Comp:         2
    #         should be:   2
    #   Int_Comp:          17
    #         should be:   17
    #   Str_Comp:          DHRYSTONE PROGRAM, SOME STRING
    #         should be:   DHRYSTONE PROGRAM, SOME STRING
    # Next_Ptr_Glob->
    #   Ptr_Comp:          24027536
    #         should be:   (implementation-dependent), same as above
    #   Discr:             0
    #         should be:   0
    #   Enum_Comp:         1
    #         should be:   1
    #   Int_Comp:          18
    #         should be:   18
    #   Str_Comp:          DHRYSTONE PROGRAM, SOME STRING
    #         should be:   DHRYSTONE PROGRAM, SOME STRING
    # Int_1_Loc:           5
    #         should be:   5
    # Int_2_Loc:           13
    #         should be:   13
    # Int_3_Loc:           7
    #         should be:   7
    # Enum_Loc:            1
    #         should be:   1
    # Str_1_Loc:           DHRYSTONE PROGRAM, 1'ST STRING
    #         should be:   DHRYSTONE PROGRAM, 1'ST STRING
    # Str_2_Loc:           DHRYSTONE PROGRAM, 2'ND STRING
    #         should be:   DHRYSTONE PROGRAM, 2'ND STRING
    #
    # Microseconds for one run through Dhrystone:  128.4
    # Dhrystones per Second:                      7786.3
    dyrystone 1000000
}

test_memspeed()
{
    # RAMspeed (GENERIC) v2.6.0 by Rhett M. Hollander and Paul V. Bolotoff, 2002-09
    #
    # 1Gb per pass mode
    #
    # INTEGER   Copy:      25.00 MB/s
    # INTEGER   Scale:     25.00 MB/s
    # INTEGER   Add:       18.75 MB/s
    # INTEGER   Triad:     18.75 MB/s
    # ---
    # INTEGER   AVERAGE:   21.88 MB/s
    ramspeed -b 3 -g 1
    # RAMspeed (GENERIC) v2.6.0 by Rhett M. Hollander and Paul V. Bolotoff, 2002-09
    #
    # 1Gb per pass mode
    #
    # FL-POINT  Copy:      16.67 MB/s
    # FL-POINT  Scale:     1.67 MB/s
    # FL-POINT  Add:       3.13 MB/s
    # FL-POINT  Triad:     1.44 MB/s
    # ---
    # FL-POINT  AVERAGE:   5.73 MB/s
    ramspeed -b 6 -g 1
}


test_interrupt()
{
    #             CPU0
    #    2:   21776655       GIC  29 Edge      twd
    #    6:      37581       GIC  55 Level     serial
    # IPI0:          0  CPU wakeup interrupts
    # IPI1:          0  Timer broadcast interrupts
    # IPI2:          0  Rescheduling interrupts
    # IPI3:          0  Function call interrupts
    # IPI4:          0  Single function call interrupts
    # IPI5:          0  CPU stop interrupts
    # IPI6:          0  IRQ work interrupts
    # IPI7:          0  completion interrupts
    #  Err:          0
    for i in `seq 10`
    do
        cat /proc/interrupts
        sleep 1
    done
}

test_all
