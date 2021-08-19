#!/bin/bash

for memory in 128; do
  echo "NodeJS, sleep 1 second, memory ${memory} MB: generate data"
  ./process.py ../../data/container_eviction/aws_nodejs_sleep_1/${memory} aws_nodejs_sleep_1_${memory}
done

for memory in 128 256 512 1024 1536; do
  echo "Python, sleep 1 second, memory ${memory} MB: generate data"
  ./process.py ../../data/container_eviction/aws_python_sleep_1/${memory} aws_python_sleep_1_${memory}
done

for memory in 128; do
  echo "Python, sleep 1 second, large package, memory ${memory} MB: generate data"
  ./process.py ../../data/container_eviction/aws_python_heavy_sleep_1/${memory} aws_python_heavy_sleep_1_${memory}
done

for memory in 128 1536; do
  echo "Python, sleep 10 seconds, large package, memory ${memory} MB: generate data"
  ./process.py ../../data/container_eviction/aws_python_sleep_10/${memory} aws_python_sleep_1_${memory}
done

echo "Generate plots"
Rscript plot.R

