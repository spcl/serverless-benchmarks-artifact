#!/bin/bash

echo "Execute benchmark uploader, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config uploader.json --output-dir uploader --cache cache

echo "Execute benchmark thumbnailer, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config thumbnailer_py.json --output-dir thumbnailer_py --cache cache

echo "Execute benchmark thumbnailer, NodeJS"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config thumbnailer_node.json --output-dir thumbnailer_node --cache cache

echo "Execute benchmark compression, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config compression.json --output-dir compression --cache cache

echo "Execute benchmark image-recognition, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config image-recognition.json --output-dir image-recognition --cache cache

echo "Execute benchmark graph-bfs, Python"
../../../serverless-benchmarks/sebs.py experiment invoke perf-cost --config graph-bfs.json --output-dir graph-bfs --cache cache

