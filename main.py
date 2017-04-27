#!/usr/bin/env python3

import csv

from datetime import datetime

from testing.cba import CoolBananasAPI
from testing.ffs import FFSAPI

def main():
    NUM_RUNS = 5

    cba = CoolBananasAPI()
    ffs = FFSAPI()

    with open('timingResults.csv', 'w') as csvfile:
        fieldnames = ['test_number', 'ffs_ave_time', 'cba_ave_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        test_number = 0
        for test_case in test_cases:
            test_number += 1
            printTest(test_case)
            cbares = cba.query(*test_case)
            ffsres = ffs.query(*test_case)

            print(cbares)
            print()
            print(ffsres)
            print()

            ffs_ave = 0
            cba_ave = 0
            for i in range(1, NUM_RUNS):
                cba_test_run = cba.query(*test_case)
                ffs_test_run = ffs.query(*test_case)
                if (cba_test_run.time):
                    cba_ave = cba_ave + float(cba_test_run.time)
                if (ffs_test_run.time):
                    ffs_ave = ffs_ave + float(ffs_test_run.time.replace(" seconds", ""))
            ffs_ave = ffs_ave / NUM_RUNS
            cba_ave = ffs_ave / NUM_RUNS
            if (ffs_ave == 0):
                ffs_ave = "error" # when no timing results have been provided
            if (cba_ave == 0):
                cba_ave = "error"
            

            writer.writerow({'test_number': test_number,
                'ffs_ave_time': ffs_ave,
                'cba_ave_time': cba_ave})



def printTest(test_case):
    print('RICs:       ', test_case[0])
    print('Topic Codes:', test_case[1])
    print('Start Date: ', test_case[2])
    print('End Date:   ', test_case[3])
    print()


test_cases = [
    # Test 1: Date range (test a two month range, then a four month, etc.)
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-03-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-05-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-07-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-09-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-11-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-03-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-05-01T00:00:00.000Z'
    ],
    # Test 2: Adding more RICs
    [
        (),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX',),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', '601088.SS'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', '601088.SS', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', '601088.SS', 'BLT.L', 'VALE5.SA'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', '601088.SS', 'BLT.L', 'VALE5.SA', 'GLEN.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    # Test 3: Adding more topic codes.
    [
        ('BHP.AX', 'BLT.L'),
        (),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('AMERS',),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('AMERS', 'AU'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('AMERS', 'AU', 'COM'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('AMERS', 'AU', 'COM', 'ENER'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('AMERS', 'AU', 'COM', 'ENER', 'NZ'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    # Test 4: Bad inputs
    [
        ('BHP.AX', 'BLT.L'),
        ('AMERS', 'COM'),
        '2016-01-01T00:00:00.000Z',
        '2015-01-01T00:00:00.000Z'
    ],
    [
        ('                   '),
        ('AMERS', 'COM'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('                '),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
]

if __name__ == '__main__':
    main()