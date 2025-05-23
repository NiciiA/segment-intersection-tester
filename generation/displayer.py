import csv
import itertools
from decimal import Decimal, getcontext
from collections import namedtuple
import matplotlib.pyplot as plt
import argparse
import struct

# Increase precision for Decimal calculations
getcontext().prec = 100

# Define Point and Segment structures
Point = namedtuple('Point', 'x y')
Segment = namedtuple('Segment', 'p1 p2')


def bin2float(binary_string, single=False):
    if len(binary_string) != (32 if single else 64):
        raise ValueError("Binary string length must be 32 (for float) or 64 (for double).")
    byte_data = int(binary_string, 2).to_bytes(4 if single else 8, byteorder='big')
    return struct.unpack('>f' if single else '>d', byte_data)[0]


def find_intersection(seg1, seg2):
    """Calculate the intersection point(s) of two segments using Decimal."""
    x1, y1 = Decimal(seg1.p1.x), Decimal(seg1.p1.y)
    x2, y2 = Decimal(seg1.p2.x), Decimal(seg1.p2.y)
    x3, y3 = Decimal(seg2.p1.x), Decimal(seg2.p1.y)
    x4, y4 = Decimal(seg2.p2.x), Decimal(seg2.p2.y)

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        # Check for collinear overlapping segments
        if ((y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)) and ((y4 - y3) * (x1 - x3) == (y1 - y3) * (x4 - x3)):
            return find_collinear_intersections(seg1, seg2)
        return []

    num_x = ((x1 * y2 - y1 * x2) * (x3 - x4)) - ((x1 - x2) * (x3 * y4 - y3 * x4))
    num_y = ((x1 * y2 - y1 * x2) * (y3 - y4)) - ((y1 - y2) * (x3 * y4 - y3 * x4))

    inter_x = num_x / denominator
    inter_y = num_y / denominator

    # Check if the intersection point is within both segments' bounds
    if (min(x1, x2) <= inter_x <= max(x1, x2)) and (min(y1, y2) <= inter_y <= max(y1, y2)) \
            and (min(x3, x4) <= inter_x <= max(x3, x4)) and (min(y3, y4) <= inter_y <= max(y3, y4)):
        return [Point(inter_x, inter_y)]
    return []


def find_collinear_intersections(seg1, seg2):
    """Check for overlapping points when segments are collinear."""
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


def calculate_intersections(segments):
    intersections = []
    for seg1, seg2 in itertools.combinations(segments, 2):
        intersection_points = find_intersection(seg1, seg2)
        intersections.extend(intersection_points)
    return intersections

def load_segments_from_csv(filepath):
    segments = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            p1 = Point(Decimal(bin2float(row['x1'])), Decimal(bin2float(row['y1'])))
            p2 = Point(Decimal(bin2float(row['x2'])), Decimal(bin2float(row['y2'])))
            segments.append(Segment(p1, p2))
    return segments


def plot_segments_and_intersections(segments, intersections):
    plt.figure(figsize=(8, 8))

    # Plot the segments
    for segment in segments:
        plt.plot([float(segment.p1.x), float(segment.p2.x)], [float(segment.p1.y), float(segment.p2.y)], 'b-',
                 label='Segment')

    # Plot the intersections
    for intersection in intersections:
        plt.plot(float(intersection.x), float(intersection.y), 'ro', label='Intersection')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Segments and Intersections')
    plt.grid(True)
    plt.show()


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Find and plot intersections from a CSV file.')
    parser.add_argument('-f', '--file', required=True, help='Path to the CSV file containing segments.')
    parser.add_argument('-d', '--display', action='store_true', help='Display the plot of segments and intersections.')

    args = parser.parse_args()

    # Load segments from the CSV file
    segments = load_segments_from_csv(args.file)

    # Calculate intersections
    intersections = calculate_intersections(segments)

    def distinct_intersections(intersections_array):
        points = set()
        for point in intersections_array:
            p_x, p_y = point
            points.add((p_x, p_y))
        return sorted(points, key=lambda p: (p[0], p[1]))

    distinct_intersection = distinct_intersections(intersections)

    print(str(len(intersections)))
    print(str(len(distinct_intersection)))

    # Plot the results
    if args.display:
        plot_segments_and_intersections(segments, intersections)


if __name__ == '__main__':
    main()
