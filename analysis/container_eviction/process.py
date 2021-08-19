#!/usr/bin/env python3

import csv
import glob
import json
import logging
import os
import sys
import operator

check_dir = sys.argv[1]
result_dir = sys.argv[2]

# Header: Memory Sleep Invocations DeltaT WarmContainers
data = []
for dir in [check_dir]:

    found_values = {}
    for results in os.listdir(dir):
        if results != 'logs':
            invocations = results.split('_')[0]
            for data_file in glob.glob(os.path.join(dir, results, '010_sleep_*')):
                try:
                    print(data_file)
                    json_data = json.load(open(data_file, 'r'))

                    sleep_time = json_data['sleep_time']
                    memory = json_data['memory']
                    invocations = json_data['invocations']
                    repetitions = json_data['repetition']
                    found_times = []
                    for key, val in json_data['results'].items():
                        found_times.append(key)

                        if len(val) != repetitions:
                            logging.warning('Invocations {} Time {} Only {} reps!'.format(invocations, key, len(val)))

                        for repetition in val:
                            assert len(repetition) == invocations
                            cold_containers = 0
                            for invocation in repetition:
                                #print(invocation)
                                is_cold = invocation['second_result']['cold']
                                if is_cold:
                                    cold_containers += 1
                            warm_containers = invocations - cold_containers
                            data.append([memory, sleep_time, invocations, key, warm_containers])
                    if invocations in found_values:
                        found_values[invocations].extend(found_times)
                    else:
                        found_values[invocations] = found_times
                except Exception as ex:
                    print(ex)
                    print(data_file)
expected_times = 28
for key, val in found_values.items():
    if len(val) != expected_times:
        logging.warning('Invocations {} Only these values {} !'.format(key, val))

data = sorted(data, key=lambda x : list(map(int, operator.itemgetter(2,3,4)(x))))

with open('results_{}_{}_{}.csv'.format(result_dir, memory, sleep_time), 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Memory', 'FunctionTime','Invocations','DeltaT','WarmContainers'])
    for row in data:
        writer.writerow(row)
#print(data)
