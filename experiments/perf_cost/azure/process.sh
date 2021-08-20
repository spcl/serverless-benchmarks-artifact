#!/bin/bash

echo "Execute benchmark uploader, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config uploader.json --output-dir uploader

echo "Execute benchmark thumbnailer, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config thumbnailer_py.json --output-dir thumbnailer_py 

#echo "Execute benchmark thumbnailer, NodeJS"
#../../../serverless-benchmarks/sebs.py experiment process perf-cost --config thumbnailer_node.json --output-dir thumbnailer_node 

echo "Execute benchmark compression, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config compression.json --output-dir compression

echo "Execute benchmark image-recognition, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config image-recognition.json --output-dir image-recognition 

echo "Execute benchmark graph-bfs, Python"
../../../serverless-benchmarks/sebs.py experiment process perf-cost --config graph-bfs.json --output-dir graph-bfs

