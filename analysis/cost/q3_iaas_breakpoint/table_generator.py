#!/usr/bin/env python3

from os.path import pardir, join
import pandas as pd
import numpy as np

# this data is taken from faas_cost.txt
# manually select the 'eco' - lowest cost
# manually select the 'perf' - same as Table 5 (reach plateau)

# Data from perf/q4
iaas_minio = np.array([0.2165095, 0.045406999999999996, 0.16591621850000002, 0.8085115, 0.203863, 0.030183])
iaas_s3 = np.array([0.31658949999999997, 0.13089499999999998, 0.19129641100000003, 2.8034025000000002, 0.2351085, 0.030729])

with open('final_table.txt', 'w') as f:

    # Data from faas_cost.txt
    medians_gbs = {
        '120': 0.2125, #128
        '210': 0.1375, #128
        '210_n': 0.225, #128
        '311': 1.925, #256
        '411': 0.950, #512
        '503': 0.125, #256
    }
    print('FaaS Eco', file=f)
    eco_cost = []
    eco_be = []
    for problem, cost in medians_gbs.items():
        print(f"Problem {problem}", file=f)
        print(f"Cost of 1M requests: {cost*0.0000166667*1000*1000}", file=f)
        print(f"Break-even point: {0.0116/(cost*0.0000166667)}", file=f)
        eco_cost.append(cost*0.0000166667*1000*1000)
        eco_be.append(0.0116/(cost*0.0000166667))

    print('Best!', file=f)
    # Data from faas_cost.txt
    best_gbs = {
        '120': 0.4,
        '210': 0.2, #256
        '210_n': 0.6, #128
        '311': 3.0, #1024
        '411': 1.175, #512
        '503': 0.15, #256
    }
    perf_cost = []
    perf_be = []
    for problem, cost in best_gbs.items():
        print(f"Problem {problem}", file=f)
        print(f"Cost of 1M requests: {cost*0.0000166667*1000*1000}", file=f)
        print(f"Break-even point: {0.0116/(cost*0.0000166667)}", file=f)
        perf_cost.append(cost*0.0000166667*1000*1000)
        perf_be.append(0.0116/(cost*0.0000166667))

    print('Table', file=f)
    print('Local', 3600 / iaas_minio, file=f)
    print('S3', 3600 / iaas_s3, file=f)
    print('Eco cost', eco_cost, file=f)
    print('Eco Break-Even', eco_be, file=f)
    print('Perf cost', perf_cost, file=f)
    print('Perf Break-Even', perf_be, file=f)

