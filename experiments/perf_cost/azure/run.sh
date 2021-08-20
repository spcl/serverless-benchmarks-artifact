#!/bin/bash

echo "Execute benchmark uploader, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config uploader.json --output-dir uploader --cache cache --output-file run.log

echo "Execute benchmark thumbnailer, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config thumbnailer_py.json --output-dir thumbnailer_py --cache cache --output-file run.log

# Func Apps 2.0 cannot be created with Node runtime anymore
#echo "Execute benchmark thumbnailer, NodeJS"
#../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config thumbnailer_node.json --output-dir thumbnailer_node --cache cache --output-file run.log

echo "Execute benchmark compression, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config compression.json --output-dir compression --cache cache --output-file run.log

echo "Execute benchmark image-recognition, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config image-recognition.json --output-dir image-recognition --cache cache --output-file run.log

echo "Execute benchmark graph-bfs, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config graph-bfs.json --output-dir graph-bfs --cache cache --output-file run.log

