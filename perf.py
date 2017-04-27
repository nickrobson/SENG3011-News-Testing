#!/usr/bin/env python3

import math
import threading
import time

from testing.cba import CoolBananasAPI
from testing.ffs import FFSAPI

NUM_RUNS = 5

def test_api(api, test_case):
    query_time = 0
    for run in range(NUM_RUNS):
        print('    Run #', run + 1, sep='')
        results = api.query(*test_case)
        if results.success:
            query_time += results.time
        else:
            query_time = float('nan')
            print('       ', results.error)
    return query_time


def main():
    for api in [CoolBananasAPI(), FFSAPI()]:
        print('Starting testing on', type(api).__name__)
        total_time = 0
        query_time = 0
        for i, test_case in enumerate(test_cases):
            print('Test case #', i + 1, sep='')
            start = time.perf_counter()
            this_query_time = test_api(api, test_case)
            this_total_time = time.perf_counter() - start
            query_time += this_query_time
            total_time += this_total_time
            if math.isnan(this_query_time):
                print('    Could not track query time as there were errors')
            else:
                print('    Took', this_query_time, 'query time')
                print('    Took', this_query_time / NUM_RUNS, 'query time, on average.')
            print('    Took', this_total_time, 'total time.')
            print('    Took', this_total_time / NUM_RUNS, 'total time, on average.')
        if math.isnan(query_time):
            print('Could not track query time as there were errors.')
        else:
            print('Took', query_time, 'query time.')
            print('Took', query_time / len(test_cases) / NUM_RUNS, 'query time, on average.')
        print('Took', total_time, 'total time.')
        print('Took', total_time / len(test_cases) / NUM_RUNS, 'total time, on average.')

test_cases = [
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2015-10-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX', 'BLT.L'),
        ('COM', 'AMERS'),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        (),
        ('COM',),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ],
    [
        ('BHP.AX',),
        (),
        '2015-01-01T00:00:00.000Z',
        '2016-01-01T00:00:00.000Z'
    ]
]

if __name__ == '__main__':
    main()