#!/usr/bin/env python3

import os
import math
import sys
from typing import List, Tuple
from collections import namedtuple

import numpy as np
import scipy.stats as st
from scipy.stats import norm
import pandas as pd

SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

BasicStats = namedtuple('BasicStats', 'mean median std cv')

def basic_stats(times: List[float]) -> BasicStats:
    mean = np.mean(times)
    median = np.median(times)
    std = np.std(times)
    cv = std / mean * 100
    return BasicStats(mean, median, std, cv)

def ci_tstudents(alpha: float, times: List[float]) -> Tuple[float, float]:
    mean = np.mean(times)
    return st.t.interval(
        alpha, len(times) - 1, loc=mean, scale=st.sem(times)
    )


def ci_le_boudec(alpha: float, times: List[float]) -> Tuple[float, float]:

    sorted_times = sorted(times)
    n = len(times)

    # z(alfa/2)
    z_value = {
        0.95: 1.96,
        0.99: 2.576
    }.get(alpha)

    low_pos = math.floor( (n - z_value * math.sqrt(n)) / 2)
    high_pos = math.ceil( 1 + (n + z_value * math.sqrt(n)) / 2)

    return (sorted_times[low_pos], sorted_times[high_pos])

warm = []
cold = []

def process(dir:str):
    dir = os.path.join(sys.argv[1], dir)
    print(os.path.relpath(dir, SCRIPTPATH), "warm")
    x = pd.read_csv(os.path.join(dir, "time_warm/instance_0/results/time_warm_00.csv"), header=[0], comment="#")
    x["Duration"] = x["Duration"] / 1000.0
    mean, median, std, cv= basic_stats(x["Duration"])
    print(f"Mean {mean}, median {median}, std {std}, CV {cv}")
    req = 60*60.0/(median/1000.0)
    print(f"Requests per hour {req}, cost per 1M requests {1000*1000*0.0116/req}")
    warm.append(median / 1000.0)
    for alpha in [0.95, 0.99]:
        ci_interval = ci_le_boudec(alpha, x["Duration"])
        interval_width = ci_interval[1] - ci_interval[0]
        ratio = 100 * interval_width / median / 2.0
        print(
            f"Non-parametric CI {alpha} from {ci_interval[0]} to {ci_interval[1]}, within {ratio}% of median"
        )

    print(os.path.relpath(dir, SCRIPTPATH), "cold")
    x = pd.read_csv(os.path.join(dir, "time_cold/instance_0/results/time_cold_00.csv"), header=[0], comment="#")
    x["Wallclock"] = x["Wallclock"] * 1000.0
    mean, median, std, cv= basic_stats(x["Wallclock"])
    print(f"Mean {mean}, median {median}, std {std}, CV {cv}")
    cold.append(median / 1000.0)
    for alpha in [0.95, 0.99]:
        ci_interval = ci_le_boudec(alpha, x["Wallclock"])
        interval_width = ci_interval[1] - ci_interval[0]
        ratio = 100 * interval_width / median / 2.0
        print(
            f"Non-parametric CI {alpha} from {ci_interval[0]} to {ci_interval[1]}, within {ratio}% of median"
        )

process("120")
process("210_python")
process("210_node")
process("311")
process("411")
process("503")

print(f"Paper table data, warm {warm}")
print(f"Paper table data, cold {cold}")


