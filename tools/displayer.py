import csv
import itertools
from collections import namedtuple
import matplotlib.pyplot as plt
import argparse
import struct

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
    x1, y1 = seg1.p1.x, seg1.p1.y
    x2, y2 = seg1.p2.x, seg1.p2.y
    x3, y3 = seg2.p1.x, seg2.p1.y
    x4, y4 = seg2.p2.x, seg2.p2.y

    dx1 = x2 - x1
    dx2 = x4 - x3
    dy1 = y2 - y1
    dy2 = y4 - y3
    dx3 = x1 - x3
    dy3 = y1 - y3

    det = dx1 * dy2 - dx2 * dy1
    det1 = dx1 * dy3 - dx3 * dy1
    det2 = dx2 * dy3 - dx3 * dy2

    if det == 0:
        if det1 != 0.0 or det2 != 0.0:
            return []

        return find_collinear_intersections(seg1, seg2)

    s = det1 / det
    t = det2 / det

    if 0.0 <= s <= 1.0 and 0.0 <= t <= 1.0:
        return [Point(x1 + t * dx1, y1 + t * dy1)]
    else:
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
            p1 = Point((bin2float(row['x1'])), (bin2float(row['y1'])))
            p2 = Point((bin2float(row['x2'])), (bin2float(row['y2'])))
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
