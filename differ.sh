#!/bin/bash

BUILD_DIR=~/segment-intersection-tester/adapters/cpp/build-release/
PY_DIR=~/host/adapters/cpp/build-release/
#A=$($BUILD_DIR/test_boost-r -f "$2" | head -n 1)
#B=$($BUILD_DIR/test_cgal_arrangement-r -f "$2" | head -n 1)
A=$($BUILD_DIR/test_boost-r -a -f "$2" | sort -u | wc -l)
B=$($BUILD_DIR/test_cgal_arrangement-r -a -f "$2" | sort -u | wc -l)
#A=$(python $BUILD_DIR/test_fraction_r.py -f "$2" | head -n 1)
#B=$(python $PY_DIR/test_vectorized_r.py -f "$2" | head -n 1)

echo $A $B

if [ $A != $B ]; then
	exit 1
else
	exit 0
fi
