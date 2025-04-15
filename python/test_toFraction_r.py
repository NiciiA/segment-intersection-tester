#!/usr/bin/env python3

import argparse
import itertools
import os
import struct
from fractions import Fraction

import psutil
import time
from collections import namedtuple

# Define namedtuples
Point = namedtuple('Point', 'x y')
Segment = namedtuple('Segment', 'p1 p2')

# Function to get memory usage
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # Memory usage in bytes

# Argument parser setup
parser = argparse.ArgumentParser(description="Process a CSV file.")
parser.add_argument('-f', '--file', required=True, help='Path to the CSV file')
parser.add_argument('-a', '--accuracy', action='store_true', help='Print accuracy if this flag is set')

args = parser.parse_args()

filepath = args.file

# Validate input file
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


# Read and parse segments from the file
segments = []
with open(filepath, 'r') as file:
    next(file)  # Skip the header line
    for line in file:
        x1_bin, y1_bin, x2_bin, y2_bin = line.strip().split(';')

        # Convert binary to float and then to Fraction
        x1 = Fraction(bin2float(x1_bin))
        y1 = Fraction(bin2float(y1_bin))
        x2 = Fraction(bin2float(x2_bin))
        y2 = Fraction(bin2float(y2_bin))

        segments.append(Segment(Point(x1, y1), Point(x2, y2)))


# Function to calculate the intersection of two segments
def find_intersection(seg1, seg2):
    # Use Fraction for all calculations
    x1, y1 = seg1.p1.x, seg1.p1.y
    x2, y2 = seg1.p2.x, seg1.p2.y
    x3, y3 = seg2.p1.x, seg2.p1.y
    x4, y4 = seg2.p2.x, seg2.p2.y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        if ((y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)) and ((y4 - y3) * (x1 - x3) == (y1 - y3) * (x4 - x3)):
            return find_collinear_intersections(seg1, seg2)
        return []

    num_x = ((x1 * y2 - y1 * x2) * (x3 - x4)) - ((x1 - x2) * (x3 * y4 - y3 * x4))
    num_y = ((x1 * y2 - y1 * x2) * (y3 - y4)) - ((y1 - y2) * (x3 * y4 - y3 * x4))

    inter_x = num_x / denominator
    inter_y = num_y / denominator

    if (min(x1, x2) <= inter_x <= max(x1, x2)) and (min(y1, y2) <= inter_y <= max(y1, y2)) \
            and (min(x3, x4) <= inter_x <= max(x3, x4)) and (min(y3, y4) <= inter_y <= max(y3, y4)):
        return [Point(float(inter_x), float(inter_y))]
    return []

# Function to find collinear intersections
def find_collinear_intersections(seg1, seg2):
    points1 = sorted([seg1.p1, seg1.p2], key=lambda p: (p.x, p.y))
    points2 = sorted([seg2.p1, seg2.p2], key=lambda p: (p.x, p.y))

    if points1[1].x < points2[0].x or points2[1].x < points1[0].x:
        return []

    overlap_start = max(points1[0], points2[0], key=lambda p: (p.x, p.y))
    overlap_end = min(points1[1], points2[1], key=lambda p: (p.x, p.y))

    if overlap_start == overlap_end:
        return [overlap_start]
    else:
        return [overlap_start, overlap_end]

# Function to calculate intersections for all segment pairs
def calculate_intersections(segments):
    intersections = []
    for seg1, seg2 in itertools.combinations(segments, 2):
        intersection_points = find_intersection(seg1, seg2)
        intersections.extend(intersection_points)
    return intersections

# Main execution
initial_memory = get_memory_usage()
start_time = time.time()

# Calculate intersections
intersections = calculate_intersections(segments)
total_intersections = len(intersections)

end_time = time.time()
final_memory = get_memory_usage()

execution_time = end_time - start_time
memory_usage = final_memory - initial_memory

execution_time_ms = execution_time * 1000

# Output results
if args.accuracy:
    print("p_x;p_y")
    for point in intersections:
        print(f"{point.x};{point.y}")
else:
    print(total_intersections)
    print(int(execution_time_ms))
    print(memory_usage)
