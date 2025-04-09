#!/usr/bin/env python3
import csv
import os
import time
import argparse
import warnings
import struct

import psutil
import pandas as pd

from SweepIntersectorLib.SweepIntersector import SweepIntersector


warnings.filterwarnings("ignore", category=FutureWarning)

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # Convert bytes to MB


parser = argparse.ArgumentParser(description="Process a CSV file.")
parser.add_argument('-f', '--file', required=True, help='Path to the CSV file')
parser.add_argument('-a', '--accuracy', action='store_true', help='Print accuracy if this flag is set')

args = parser.parse_args()

filepath = args.file

if not filepath.endswith(".csv"):
    print("Error: The specified file is not a CSV file.")
    exit(1)

if not os.path.exists(filepath):
    print(f"Error: The file {filepath} does not exist.")
    exit(1)


def bin2float(binary_string, single=False):
    if len(binary_string) != (32 if single else 64):
        raise ValueError("Binary string length must be 32 (for float) or 64 (for double).")
    byte_data = int(binary_string, 2).to_bytes(4 if single else 8, byteorder='big')
    return struct.unpack('>f' if single else '>d', byte_data)[0]


segment_points = []
with open(filepath, "r") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)  # Skip the header row

    for row in reader:
        # Each row contains the binary strings
        x1 = row[0]
        y1 = row[1]
        x2 = row[2]
        y2 = row[3]

        # Convert binary strings to float and append to segment points
        segment_points.append((
            (bin2float(x1), bin2float(y1)),
            (bin2float(x2), bin2float(y2))
        ))

# print("\n=== Testing file " + filepath + " ===")

# print("\n--- Sweep Line Intersection Tests ---")
isector = SweepIntersector()

initial_memory = get_memory_usage()
start_time = time.time()

isecDic = isector.findIntersections(segment_points)

end_time = time.time()
final_memory = get_memory_usage()

execution_time = end_time - start_time
memory_usage = final_memory - initial_memory

execution_time_ms = execution_time * 1000

unique_intersections = set()

for seg, intersections in isecDic.items():
    unique_intersections.update(intersections[1:-1])

total_intersections = len(unique_intersections)

if args.accuracy:
    print("p_x;p_y")
    for point in unique_intersections:
        intersection_x = point[0]
        intersection_y = point[1]

        print(f"{intersection_x};{intersection_y}")
else:
    print(f"{total_intersections}")
    print(f"{int(execution_time_ms)}")
    print(f"{memory_usage}")

