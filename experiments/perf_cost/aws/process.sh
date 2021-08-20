#!/bin/bash

echo "Execute benchmark uploader, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config uploader.json --output-dir uploader --output-file process.log

echo "Execute benchmark thumbnailer, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config thumbnailer_py.json --output-dir thumbnailer_py --output-file process.log

echo "Execute benchmark thumbnailer, NodeJS"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config thumbnailer_node.json --output-dir thumbnailer_node --output-file process.log

echo "Execute benchmark compression, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config compression.json --output-dir compression --output-file process.log

echo "Execute benchmark image-recognition, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config image-recognition.json --output-dir image-recognition --output-file process.log

echo "Execute benchmark graph-bfs, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config graph-bfs.json --output-dir graph-bfs --output-file process.log

