#!/usr/bin/env python3

import argparse
import csv
import subprocess
import sys

from datetime import datetime

from testing.cba import CoolBananasAPI
from testing.ffs import FFSAPI

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interactive', '-i', help='Wait for user to press enter after each result before continuing.', action='store_true')
    args = parser.parse_args()
    NUM_RUNS = 5

    cba = CoolBananasAPI()
    ffs = FFSAPI()

    with open('timingResults.csv', 'w') as csvfile:
        fieldnames = ['test_number', 'ffs_ave_time', 'cba_ave_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for test_number, test_case in enumerate(test_cases):
            printTest(test_case)
            cbares = cba.query(*test_case)
            ffsres = ffs.query(*test_case)

            if not args.interactive:
                cba_ave = 0
                ffs_ave = 0
                if cbares.success:
                    cba_ave += cbares.time
                if ffsres.success:
                    ffs_ave += ffsres.time

                for i in range(1, NUM_RUNS):
                    cba_test_run = cba.query(*test_case)
                    ffs_test_run = ffs.query(*test_case)
                    if cba_test_run.success:
                        cba_ave += cba_test_run.time
                    if ffs_test_run.success:
                        ffs_ave += ffs_test_run.time

                ffs_ave /= NUM_RUNS
                cba_ave /= NUM_RUNS

                if ffs_ave == 0:
                    ffs_ave = "error" # when no timing results have been provided
                if cba_ave == 0:
                    cba_ave = "error"
            
                writer.writerow({
                    'test_number': test_number + 1,
                    'ffs_ave_time': ffs_ave,
                    'cba_ave_time': cba_ave
                })

            if cbares == ffsres:
                print('Same outputs!', file=sys.stderr)

            elif cbares.success and not ffsres.success:
                print('CBA succeeded; FFS errored', file=sys.stderr)
                print('FFS error:', ffsres.error, file=sys.stderr)
                print('CBA:', cbares)
                print('FFS:', ffsres)

            elif not cbares.success and ffsres.success:
                print('CBA errored; FFS succeeded', file=sys.stderr)
                print('CBA error:', cbares.error, file=sys.stderr)
                print('CBA:', cbares)
                print('FFS:', ffsres)

            elif not cbares.success:
                print('Both errored!', file=sys.stderr)
                print('CBA error:', cbares.error, file=sys.stderr)
                print('FFS error:', ffsres.error, file=sys.stderr)

            else:
                cba_articles = cbares.articles
                ffs_articles = ffsres.articles

                print('Both succeeded!', file=sys.stderr)
                print('CBA finished in', cbares.time, 'seconds', file=sys.stderr)
                print('FFS finished in', ffsres.time, 'seconds', file=sys.stderr)

                if len(cba_articles) != len(ffs_articles):
                    print('Different number of results!', file=sys.stderr)
                    print('CBA had', len(cba_articles), 'results', file=sys.stderr)
                    print('FFS had', len(ffs_articles), 'results', file=sys.stderr)
                    print('CBA articles:', cba_articles)
                    print('FFS articles:', ffs_articles)

                else:
                    for i, cba_article in enumerate(cba_articles):
                        ffs_article = ffs_articles[i]
                        if cba_article != ffs_article:
                            print('Article', i, 'mismatch!', file=sys.stderr)
                            print('CBA:', cba_article)
                            print('FFS:', ffs_article)

            print(file=sys.stderr)
            if args.interactive:
                input('Press [Enter] to continue.')
                subprocess.call(['clear'])


def printTest(test_case):
    print('RICs:       ', test_case[0], file=sys.stderr)
    print('Topic Codes:', test_case[1], file=sys.stderr)
    print('Start Date: ', test_case[2], file=sys.stderr)
    print('End Date:   ', test_case[3], file=sys.stderr)
    print(file=sys.stderr)


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
