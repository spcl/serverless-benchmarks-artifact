#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Memory statistics, AWS, compression"
${SCRIPT_DIR}/avg_memory_usage.py ${SCRIPT_DIR}/../../../data/performance/perf_cost/aws_perf_cost/311 > aws_compression_memory.txt
echo "-------------------------------"

echo "Memory statistics, AWS, image recognition"
${SCRIPT_DIR}/avg_memory_usage.py ${SCRIPT_DIR}/../../../data/performance/perf_cost/aws_perf_cost/411 > aws_image_recognition_memory.txt
echo "-------------------------------"
