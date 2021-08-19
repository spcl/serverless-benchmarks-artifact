#!/usr/bin/env python3

import os
from os.path import pardir, join
import pandas as pd
import numpy as np

SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

data_dir = join(SCRIPTPATH, pardir, pardir, pardir, 'data', 'performance', 'aws_perf_cost')
dirs = ['120', '210_python','210_node', '311', '411', '503']

# after data analysis, select the memory configuration when the performance stops increasing (lateau)
memory_per_benchmark = [1024,1024,2048,1024,3008,1536]
warm_faas = []
for i in range(len(dirs)):
    dir = dirs[i]
    df = pd.read_csv('{}/{}/perf-cost/result.csv'.format(data_dir,dir))

    import numpy as np
    def my_ceil(a, precision=0):
        return np.round(a + 0.5 * 10**(-precision), precision)

    print(f"Result: {dir}")
    # convert to seconds
    print('Mean provider', df.loc[(df['type'] == 'warm')].groupby(['memory']).mean()['provider_time'] / 10**6)
    print('Median provider ', df.loc[(df['type'] == 'warm')].groupby(['memory']).median()['provider_time'] / 10**6)

    warm_faas.append(df.loc[(df['type'] == 'warm')].groupby(['memory']).median()['provider_time'][memory_per_benchmark[i]])

# AWS IaaS data
# copied manually from the files aws_minio_results.txt and aws_s3_results.txt.
warm_minio = np.array([0.2165095, 0.045406999999999996, 0.16591621850000002, 0.8085115, 0.203863, 0.030183])
warm_s3 = np.array([0.31658949999999997, 0.13089499999999998, 0.19129641100000003, 2.8034025000000002, 0.2351085, 0.030729])
warm_faas = np.array(warm_faas)
# convert to seconds
warm_faas /= 10**6
overhead_minio = warm_faas / warm_minio
overhead_s3 = warm_faas / warm_s3

print('Table data', dirs)
print('minio', warm_minio)
print('s3', warm_s3)
print('faas', warm_faas)
print('overhead minio', overhead_minio)
print('overhead s3', overhead_s3)
print('memory', memory_per_benchmark)

