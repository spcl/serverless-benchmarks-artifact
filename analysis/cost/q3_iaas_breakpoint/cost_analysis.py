#!/usr/bin/env python3

import os
from os.path import pardir, join
import pandas as pd
SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

data_dir = join(SCRIPTPATH, pardir, pardir, pardir, 'data', 'performance', 'aws_perf_cost')
dirs = ['120', '210_python','210_node', '311', '411', '503']

with open('faas_cost.txt', 'w') as f:

    for i in range(len(dirs)):
        dir = dirs[i]
        df = pd.read_csv('{}/{}/perf-cost/result.csv'.format(data_dir,dir))

        import numpy as np
        def my_ceil(a, precision=0):
            return np.round(a + 0.5 * 10**(-precision), precision)

        print(f"Result: {dir}", file=f)
        from math import ceil
        time = df.loc[(df['type'] == 'warm')].groupby(['memory']).median()['provider_time'] / 10**6
        time = time.reset_index()
        time['gbs'] = time['memory'] * time['provider_time'] / 1024
        time['true_gbs'] = time['memory'] * my_ceil(time['provider_time'], 1) / 1024
        print(time, file=f)

