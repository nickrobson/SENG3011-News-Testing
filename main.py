#!/usr/bin/env python3

import argparse
import subprocess
import sys

from datetime import datetime

from testing.cba import CoolBananasAPI
from testing.ffs import FFSAPI

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interactive', '-i', help='Wait for user to press enter after each result before continuing.', action='store_true')
    args = parser.parse_args()

    cba = CoolBananasAPI()
    ffs = FFSAPI()

    for test_case in test_cases:
        printTest(test_case)
        cbares = cba.query(*test_case)
        ffsres = ffs.query(*test_case)

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
    ]
]

if __name__ == '__main__':
    main()