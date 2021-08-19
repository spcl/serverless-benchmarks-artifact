#!/usr/bin/env python3

import json
import glob
import os
import numpy as np
import sys


for f in glob.glob(os.path.join(sys.argv[1], "perf-cost","*.json")):
    if "processed" not in f:
        continue
    typ, _, mem = os.path.basename(f).split('_')
    mem = int(mem.split('-')[0])

    with open(f, 'r') as in_f:
        print(f)
        data = json.load(in_f)
        memories = []
        for req_id, invoc in next(iter(data["_invocations"].values())).items():
            mem_used = invoc["stats"]["memory_used"]
            if mem_used is not None and mem_used > 0:
                memories.append(mem_used)
        print(f"{typ}, {mem}: Mean {np.mean(memories)}, median {np.median(memories)}, min {np.min(memories)}, max {np.max(memories)}")
