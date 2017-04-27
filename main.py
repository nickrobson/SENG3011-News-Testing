#!/usr/bin/env python3

from datetime import datetime

from testing.cba import CoolBananasAPI
from testing.ffs import FFSAPI

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
    ],,
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
]

def main():
    cba = CoolBananasAPI()
    ffs = FFSAPI()

    for test_case in test_cases:
        cbares = cba.query(*test_case)
        ffsres = ffs.query(*test_case)

        # TODO compare the responses


if __name__ == '__main__':
    main()