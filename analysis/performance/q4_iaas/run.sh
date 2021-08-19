#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "IaaS statistics, minio"
${SCRIPT_DIR}/statistics.py ${SCRIPT_DIR}/../../../data/performance/iaas_results/aws_minio/ > aws_minio_results.txt
echo "-------------------------------"

echo "IaaS statistics, S3"
${SCRIPT_DIR}/statistics.py ${SCRIPT_DIR}/../../../data/performance/iaas_results/aws_s3/ > aws_s3_results.txt
echo "-------------------------------"
