import argparse
import concurrent.futures
import math
import os
import random
import itertools
import csv
from fractions import Fraction

import matplotlib.pyplot as plt
from collections import namedtuple

import struct

import numpy as np

Point = namedtuple('Point', 'x y')
Segment = namedtuple('Segment', 'p1 p2')

near_inf = math.nextafter(math.inf, -math.inf)


def float2bin(number, hexdecimal=False, single=False):
    bytes_data = struct.pack('>f' if single else '>d', number)
    func, length = (hex, 2) if hexdecimal else (bin, 8)
    byte2bin = lambda byte: func(byte)[2:].rjust(length, '0')
    return ''.join(map(byte2bin, bytes_data))


def parallel_and_collinear_1():
    """
        Testing how it handles parallel segments closely
    """
    segments = [Segment(Point(10, 50), Point(90, 50))]

    next_value = math.nextafter(50.0, math.inf)

    segments.append(Segment(Point(10, next_value),
                            Point(90, next_value)))

    return segments


def parallel_and_collinear_2():
    """
        Testing how it handles parallel segments slightly shifted
    """
    segments = [Segment(Point(11, 50), Point(91, 50))]

    next_value = math.nextafter(50.0, math.inf)

    segments.append(Segment(Point(9, next_value),
                            Point(89, next_value)))

    return segments


def parallel_and_collinear_3():
    """
        Testing how it handles collinear segments
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(10, 50), Point(90, 50))]

    return segments


def parallel_and_collinear_4():
    """
        Testing how it handles collinear segments slightly shifted
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(9, 50), Point(89, 50))]

    return segments


def parallel_and_collinear_5():
    """
        Testing how it handles collinear segments slightly tilted
    """
    segments = [Segment(Point(10, 10), Point(90, 90)),
                Segment(Point(9, 9), Point(91, 91))]

    return segments


def parallel_and_collinear_6():
    """
        Testing how it handles parallel segments slightly tilted
    """
    segments = [Segment(Point(10, 10), Point(90, 90)),
                Segment(Point(10, 12), Point(90, 92))]

    return segments


def parallel_and_collinear_7():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(10, 52), Point(90, 52))]

    return segments


def parallel_and_collinear_8():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(50, 10), Point(50, 90))]

    return segments


def parallel_and_collinear_9():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(10, 40), Point(90, 50))]

    return segments


def parallel_and_collinear_10():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(10, 50), Point(90, 40))]

    return segments


def parallel_and_collinear_11():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(-1, -2), Point(1, 2)),
                Segment(Point(-2, 2), Point(2, -2)),
                Segment(Point(-2, -2), Point(0, 0))]

    return segments


def parallel_and_collinear_12():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(0, 0), Point(2, 0)),
                Segment(Point(3, 0), Point(5, 0))]

    return segments


def parallel_and_collinear_13():
    """
        Testing how it handles parallel segments
    """
    segments = [Segment(Point(0, 0), Point(0, 0)),
                Segment(Point(1, 1), Point(1, 1))]

    return segments


def parallel_and_collinear_14():
    """
        Testing how it handles parallel segments closely, by two
    """
    segments = [Segment(Point(10, 50), Point(90, 50))]

    next_value = math.nextafter(50.0, math.inf)
    next_value = math.nextafter(next_value, math.inf)

    segments.append(Segment(Point(10, next_value),
                            Point(90, next_value)))

    return segments


def parallel_and_collinear_15():
    """
        Testing how it handles parallel segments closely, by three
    """
    segments = [Segment(Point(10, 50), Point(90, 50))]

    next_value = math.nextafter(50.0, math.inf)
    next_value = math.nextafter(next_value, math.inf)
    next_value = math.nextafter(next_value, math.inf)

    segments.append(Segment(Point(10, next_value),
                            Point(90, next_value)))

    return segments


def parallel_and_collinear_16():
    """
        Testing how it handles parallel segments closely, by four
    """
    segments = [Segment(Point(10, 50), Point(90, 50))]

    next_value = math.nextafter(50.0, math.inf)
    next_value = math.nextafter(next_value, math.inf)
    next_value = math.nextafter(next_value, math.inf)
    next_value = math.nextafter(next_value, math.inf)

    segments.append(Segment(Point(10, next_value),
                            Point(90, next_value)))

    return segments


def parallel_and_collinear_17():
    """
        Testing how it handles vertically parallel segments
    """
    segments = [Segment(Point(50, 10), Point(50, 90)),
                Segment(Point(50, 10), Point(50, 90))]

    return segments


def parallel_and_collinear_18():
    """
        Testing how it handles vertically parallel segments closely, by one
    """
    segments = [Segment(Point(50, 10), Point(50, 90))]

    next_value = math.nextafter(50.0, math.inf)

    segments.append(Segment(Point(next_value, 10),
                            Point(next_value, 80)))

    return segments


def parallel_and_collinear_19():
    """
        Testing how it handles vertically parallel segments closely, by two
    """
    segments = [Segment(Point(50, 10), Point(50, 90))]

    next_value = math.nextafter(50.0, math.inf)
    next_value = math.nextafter(next_value, math.inf)

    segments.append(Segment(Point(next_value, 10),
                            Point(next_value, 80)))

    return segments


def parallel_and_collinear_20():
    """
        Testing how it handles vertically parallel segments closely, by three
    """
    segments = [Segment(Point(50, 10), Point(50, 90))]

    next_value = math.nextafter(50.0, math.inf)
    next_value = math.nextafter(next_value, math.inf)
    next_value = math.nextafter(next_value, math.inf)

    segments.append(Segment(Point(next_value, 10),
                            Point(next_value, 80)))

    return segments


def length_0_1():
    """
        Testing how it handles a single length-0 segment (Precondition)
    """
    segments = [Segment(Point(50, 50), Point(50, 50))]

    return segments


def length_0_2():
    """
        Testing how it handles two intersecting length-0 segments
    """
    segments = [Segment(Point(50, 50), Point(50, 50)),
                Segment(Point(50, 50), Point(50, 50))]

    return segments


def length_0_3():
    """
        Testing how it handles a segment intersecting with a length-0 segment
    """
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(50, 50), Point(50, 50))]

    return segments


def length_0_4():
    """
        Testing how it handles a segment intersecting with a length-0 segment
    """
    segments = [Segment(Point(50, 50), Point(50, 50)),
                Segment(Point(10, 50), Point(90, 50))]

    return segments


def star_intersections_1():
    segments = [Segment(Point(30, 10), Point(70, 90)),
                Segment(Point(10, 10), Point(90, 90)),
                Segment(Point(90, 10), Point(10, 90))]

    return segments


def star_intersections_2():
    next_value = math.nextafter(10.0, math.inf)

    segments = [Segment(Point(30, 10), Point(70, 90)),
                Segment(Point(10, 10), Point(90, 90)),
                Segment(Point(90, next_value), Point(10, 90))]

    return segments


def star_intersections_3():
    segments = [Segment(Point(20, 10), Point(80, 90)),
                Segment(Point(30, 10), Point(70, 90)),
                Segment(Point(40, 10), Point(60, 90)),
                Segment(Point(60, 10), Point(40, 90)),
                Segment(Point(70, 10), Point(30, 90)),
                Segment(Point(80, 10), Point(20, 90)),
                Segment(Point(10, 10), Point(90, 90)),
                Segment(Point(10, 90), Point(90, 10))]

    return segments


def star_intersections_4(num_segments: int, max_coord: float):
    segments = []

    center = Point(max_coord / 2, max_coord / 2)

    angle_step = 2 * math.pi / num_segments

    for i in range(num_segments):
        angle = i * angle_step

        end_x = center.x + max_coord * math.cos(angle)
        end_y = center.y + max_coord * math.sin(angle)

        end_point = Point(end_x, end_y)

        if (center.x > end_point.x) or (center.x == end_point.x and center.y > end_point.y):
            segments.append(Segment(end_point, center))
        else:
            segments.append(Segment(center, end_point))

    return segments


def star_intersections_5():
    segments = [Segment(Point(10, 10), Point(90, 90)),
                Segment(Point(10, 90), Point(90, 10))]

    return segments


def star_intersections_6(num_segments: int, max_coord: float):
    segments = []

    # Generate points along the left and right boundaries
    left_points = []
    right_points = []

    # Add random points on the left and right side
    for _ in range(num_segments):
        left_points.append(Point(10, random.randint(10, int(max_coord))))
        right_points.append(Point(max_coord - 10, random.randint(10, int(max_coord))))

    random.shuffle(left_points)
    random.shuffle(right_points)

    # Create the segments between the points on the left and right
    for i in range(num_segments):
        left_point = left_points[i]
        right_point = right_points[i]

        segments.append(Segment(left_point, right_point))

    return segments


def star_intersections_7(num_segments: int, max_coord: float):
    return star_intersections_shaped(num_segments, max_coord, num_segments // 2)


def star_intersections_8(num_segments: int, max_coord: float):
    return star_intersections_shaped_r(num_segments, max_coord, num_segments // 2)


def star_intersections_shaped(num_segments: int, max_coord: float, skip: int):
    segments = []

    points = []

    # Calculate the angle step for evenly spaced points on the circle
    angle_step = 2 * math.pi / num_segments

    # Generate points evenly spaced around the circle
    for i in range(num_segments):
        angle = i * angle_step
        x = max_coord / 2 * math.cos(angle) + max_coord / 2  # Centered at (max_coord / 2, max_coord / 2)
        y = max_coord / 2 * math.sin(angle) + max_coord / 2  # Centered at (max_coord / 2, max_coord / 2)
        points.append(Point(x, y))

    # Create segments by skipping a specified number of points (creating a star shape)
    for i in range(num_segments):
        start_point = points[i]
        # Calculate the index of the point to connect to, based on the 'skip' value
        end_point = points[(i + skip) % num_segments]
        segments.append(Segment(start_point, end_point))

    return segments


def star_intersections_shaped_r(num_segments: int, max_coord: float, skip: int):
    segments = []

    points = []

    # Calculate the angle step for evenly spaced points on the circle
    angle_step = 2 * math.pi / num_segments

    # Generate points evenly spaced around the circle
    for i in range(num_segments):
        angle = i * angle_step
        x = max_coord / 2 * math.cos(angle) + max_coord / 2  # Centered at (max_coord / 2, max_coord / 2)
        y = max_coord / 2 * math.sin(angle) + max_coord / 2  # Centered at (max_coord / 2, max_coord / 2)

        if random.random() < 0.8:
            if random.random() < 0.6:
                x = math.nextafter(x, math.inf)
            else:
                x = math.nextafter(x, -math.inf)

        if random.random() < 0.8:
            if random.random() < 0.6:
                y = math.nextafter(y, math.inf)
            else:
                y = math.nextafter(y, -math.inf)

        points.append(Point(x, y))

    # Create segments by skipping a specified number of points (creating a star shape)
    for i in range(num_segments):
        start_point = points[i]
        # Calculate the index of the point to connect to, based on the 'skip' value
        end_point = points[(i + skip) % num_segments]
        segments.append(Segment(start_point, end_point))

    return segments


def star_intersections_9(num_segments: int, num_intersections: int, max_coord: float):
    segments = []

    # Generate equally spaced y-coordinates for horizontal segments
    y_spacing = max_coord / (num_segments + 1)
    left_points = [Point(10, y_spacing * (i + 1)) for i in range(num_segments)]
    right_points = [Point(max_coord - 10, y_spacing * (i + 1)) for i in range(num_segments)]

    # Initially create horizontal segments
    for i in range(num_segments):
        segments.append(Segment(left_points[i], right_points[i]))

    # Adjust segments to reach the desired number of intersections
    intersections = calculate_intersections_d(segments)

    while len(intersections) != num_intersections:
        i, j = random.sample(range(num_segments), 2)

        # Modify endpoints
        original_segment_i, original_segment_j = segments[i], segments[j]

        segments[i] = Segment(segments[i].p1, segments[j].p2)
        segments[j] = Segment(segments[j].p1, segments[i].p2)

        # Recalculate intersections
        new_intersections = calculate_intersections_d(segments)

        if len(new_intersections) > num_intersections:
            # Revert if too many intersections
            segments[i] = original_segment_i
            segments[j] = original_segment_j
        else:
            intersections = new_intersections

    return segments


def multi_axis_1():
    segments = [Segment(Point(10, 10), Point(10, 90))]

    return segments


def multi_axis_2():
    segments = [Segment(Point(10, 10), Point(90, 10))]

    return segments


def multi_axis_3():
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(50, 10), Point(50, 90))]

    return segments


def multi_axis_4():
    segments = [Segment(Point(10, 50), Point(50, 50)),
                Segment(Point(50, 10), Point(50, 50)),
                Segment(Point(50, 50), Point(90, 50)),
                Segment(Point(50, 50), Point(50, 90))]

    return segments


def multi_axis_5():
    segments = [Segment(Point(10, 50), Point(90, 50)),
                Segment(Point(50, 10), Point(50, 50)),
                Segment(Point(50, 50), Point(50, 90))]

    return segments


def multi_axis_6():
    segments = [Segment(Point(10, 50), Point(50, 50)),
                Segment(Point(50, 10), Point(50, 90))]

    return segments


def multi_axis_7():
    segments = [Segment(Point(10, 10), Point(50, 10)),
                Segment(Point(50, 10), Point(50, 90))]

    return segments


def multi_axis_8():
    segments = [Segment(Point(10, 90), Point(50, 90)),
                Segment(Point(50, 10), Point(50, 90))]

    return segments


def clustered_x(num_segments: int, max_coord: float, cluster_center_num: int):
    """
        Generates segments clustered around several random centers in the coordinate space with high intersections.
    """
    segments = []

    # Generate random cluster centers
    cluster_centers = [
        (random.uniform(0.2 * max_coord, 0.8 * max_coord), random.uniform(0.2 * max_coord, 0.8 * max_coord))
        for _ in range(cluster_center_num)
    ]

    # Define a smaller radius around the cluster center where the segments will be generated
    cluster_radius = max_coord * 0.1  # 10% of the total max_coord as the cluster radius

    # Split the total number of segments roughly equally between clusters
    segments_per_cluster = num_segments // cluster_center_num
    remaining_segments = num_segments % cluster_center_num  # Handle any extra segments

    for center_x, center_y in cluster_centers:
        # Generate segments around each cluster center
        for _ in range(segments_per_cluster + (1 if remaining_segments > 0 else 0)):
            # Decrease the remaining_segments after using it for a cluster
            if remaining_segments > 0:
                remaining_segments -= 1

            # Generate two random points within the cluster radius
            # To force more intersections, we generate more segments that share a common center or cross paths
            p1 = Point(
                random.uniform(center_x - cluster_radius, center_x + cluster_radius),
                random.uniform(center_y - cluster_radius, center_y + cluster_radius)
            )
            p2 = Point(
                random.uniform(center_x - cluster_radius, center_x + cluster_radius),
                random.uniform(center_y - cluster_radius, center_y + cluster_radius)
            )

            # Create the segment from these points and add to the list
            if (p1.x > p2.x) or (p1.x == p2.x and p1.y > p2.y):
                segments.append(Segment(p2, p1))
            else:
                segments.append(Segment(p1, p2))

    return segments


def rounding(num_segments: int, max_coord_x=100.0, max_coord_y=100.0):
    segments = [Segment(Point(0, (max_coord_y * 0.8)), Point(max_coord_x, (max_coord_y * 0.9)))]

    x_positions = np.linspace(10, int(max_coord_x * 0.9), num_segments)
    for x in x_positions:
        segments.append(Segment(Point(x, 5), Point(x, max_coord_y * 0.85)))

    return segments


def accuracy_1():
    return [Segment(Point(0, 0), Point(near_inf, 0)),
            Segment(Point(0, 0), Point(0, -near_inf))]


def accuracy_2():
    return [Segment(Point(0, 0), Point(near_inf, 1)),
            Segment(Point(0, 1), Point(1, 1))]


def accuracy_3():
    return [Segment(Point(0, 0), Point(near_inf, near_inf)),
            Segment(Point(0, 0), Point(1, 1))]


def accuracy_4():
    return [Segment(Point(0, 0), Point(near_inf, near_inf)),
            Segment(Point(0, 1), Point(1, 2))]


def accuracy_5():
    return [Segment(Point(-near_inf, 0), Point(near_inf, 0)),
            Segment(Point(0, 1), Point(0, -1))]


def accuracy_6():
    return [Segment(Point(-near_inf, -near_inf), Point(near_inf, near_inf)),
            Segment(Point(near_inf, near_inf), Point(-near_inf, -near_inf))]


def accuracy_7():
    return [Segment(Point(-near_inf, 0), Point(near_inf, 0)),
            Segment(Point(-1, 1), Point(1, -1))]


def accuracy_8():
    return [Segment(Point(0, -near_inf), Point(0, near_inf)),
            Segment(Point(0, 1), Point(0, -1))]


def accuracy_9():
    return [Segment(Point(0, -near_inf), Point(0, near_inf)),
            Segment(Point(-1, 0), Point(1, 0))]


def accuracy_10():
    return [Segment(Point(0, -near_inf), Point(0, near_inf)),
            Segment(Point(-1, -1), Point(1, 1))]


def generate_random_point(max_coord=100.0):
    return Point(random.uniform(0, max_coord), random.uniform(0, max_coord))


def generate_random_segment(max_coord):
    p1 = generate_random_point(max_coord)
    p2 = generate_random_point(max_coord)

    if (p1.x > p2.x) or (p1.x == p2.x and p1.y > p2.y):
        p1, p2 = p2, p1

    return Segment(p1, p2)


def find_intersection_r(seg1, seg2):
    """Calculate the intersection point(s) of two segments using Decimal."""

    x1, y1 = Fraction(seg1.p1.x), Fraction(seg1.p1.y)
    x2, y2 = Fraction(seg1.p2.x), Fraction(seg1.p2.y)
    x3, y3 = Fraction(seg2.p1.x), Fraction(seg2.p1.y)
    x4, y4 = Fraction(seg2.p2.x), Fraction(seg2.p2.y)

    denominator = (x1 - x2) * (y4 - y3) - (y1 - y2) * (x4 - x3)

    if denominator == 0:
        if ((y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)) and ((y4 - y3) * (x1 - x3) == (y1 - y3) * (x4 - x3)):
            return find_collinear_intersections(seg1, seg2)
        return []

    num_x = (x4 - x2) * (y4 - y3) - (x4 - x3) * (y4 - y2)
    num_y = (x1 - x2) * (y4 - y2) - (x4 - x2) * (y1 - y2)

    inter_x = num_x / denominator
    inter_y = num_y / denominator

    if inter_x < 0 or inter_x > 1:
        return []

    if inter_y < 0 or inter_y > 1:
        return []

    return [Point(x1 * inter_x * (x2 - x1), y1 * inter_x * (y2 - y1))]


def find_intersection_d(seg1, seg2):
    """Calculate the intersection point(s) of two segments using Decimal."""

    x1, y1 = seg1.p1.x, seg1.p1.y
    x2, y2 = seg1.p2.x, seg1.p2.y
    x3, y3 = seg2.p1.x, seg2.p1.y
    x4, y4 = seg2.p2.x, seg2.p2.y

    denominator = (x1 - x2) * (y4 - y3) - (y1 - y2) * (x4 - x3)

    if denominator == 0:
        if ((y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)) and ((y4 - y3) * (x1 - x3) == (y1 - y3) * (x4 - x3)):
            return find_collinear_intersections(seg1, seg2)
        return []

    num_x = (x4 - x2) * (y4 - y3) - (x4 - x3) * (y4 - y2)
    num_y = (x1 - x2) * (y4 - y2) - (x4 - x2) * (y1 - y2)

    inter_x = num_x / denominator
    inter_y = num_y / denominator

    if inter_x < 0 or inter_x > 1:
        return []

    if inter_y < 0 or inter_y > 1:
        return []

    return [Point(x1 * inter_x * (x2 - x1), y1 * inter_x * (y2 - y1))]


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


def calculate_intersections_d(segments):
    intersections = []
    for seg1, seg2 in itertools.combinations(segments, 2):
        intersection_points = find_intersection_d(seg1, seg2)
        intersections.extend(intersection_points)
    return intersections


def calculate_intersections_r(segments):
    intersections = []
    for seg1, seg2 in itertools.combinations(segments, 2):
        intersection_points = find_intersection_r(seg1, seg2)
        intersections.extend(intersection_points)
    return intersections


def calculate_intersections_q(intersections):
    intersections_x = []
    for intersection in intersections:
        intersections_x.append(Point(float(intersection.x), float(intersection.y)))
    return intersections_x


def accurate_intersections_d(segments):
    intersections = []
    for seg1, seg2 in itertools.combinations(segments, 2):
        intersection_points = find_intersection_d(seg1, seg2)
        for point in intersection_points:
            intersections.append((point, seg1, seg2))
    return intersections


def accurate_intersections_r(segments):
    intersections = []
    for seg1, seg2 in itertools.combinations(segments, 2):
        intersection_points = find_intersection_r(seg1, seg2)
        for point in intersection_points:
            intersections.append((point, seg1, seg2))
    return intersections


def random_x(num_segments, max_coord):
    return [generate_random_segment(max_coord) for _ in range(num_segments)]


def sort_segments(segments):
    return sorted(segments, key=lambda seg: (min(seg), max(seg)))


def save_segments_to_csv(segments, filename="segments.csv"):
    os.makedirs('tests', exist_ok=True)
    filepath = os.path.join('tests', filename)

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['x1', 'y1', 'x2', 'y2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

        segments = sort_segments(segments)

        writer.writeheader()
        for segment in segments:
            writer.writerow({'x1': str(float2bin(segment.p1.x)), 'y1': str(float2bin(segment.p1.y)), 'x2': str(float2bin(segment.p2.x)), 'y2': str(float2bin(segment.p2.y))})


def save_accuracy_to_csv(accuracies_d, accuracies_r, filename="accuracy.csv"):
    os.makedirs('tests/accuracies', exist_ok=True)
    filepath_d = os.path.join('tests/accuracies', "d_" + filename)
    filepath_r = os.path.join('tests/accuracies', "r_" + filename)

    unique_intersections_d = set()

    for intersection in accuracies_d:
        point = intersection
        unique_intersections_d.add((point.x, point.y))

    unique_intersections_r = set()

    for intersection in accuracies_r:
        point = intersection
        unique_intersections_r.add((point.x, point.y))

    sorted_intersections = sorted(unique_intersections_d, key=lambda p: (p[0], p[1]))

    with open(filepath_d, 'w', newline='') as csvfile:
        # fieldnames = ['p_x', 'p_y', 'seg1_x1', 'seg1_y1', 'seg1_x2', 'seg1_y2', 'seg2_x1', 'seg2_y1', 'seg2_x2', 'seg2_y2']
        fieldnames = ['p_x', 'p_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()
        for point_x, point_y in sorted_intersections:
            writer.writerow({
                'p_x': str(float2bin(point_x)),
                'p_y': str(float2bin(point_y))
            })

    sorted_intersections = sorted(unique_intersections_r, key=lambda p: (p[0], p[1]))

    with open(filepath_r, 'w', newline='') as csvfile:
        # fieldnames = ['p_x', 'p_y', 'seg1_x1', 'seg1_y1', 'seg1_x2', 'seg1_y2', 'seg2_x1', 'seg2_y1', 'seg2_x2', 'seg2_y2']
        fieldnames = ['p_x', 'p_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()
        for point_x, point_y in sorted_intersections:
            writer.writerow({
                'p_x': str(float2bin(point_x)),
                'p_y': str(float2bin(point_y))
            })

    # print(f"Segments saved to {filepath}")


def plot_segments_and_intersections(segments, intersections):
    plt.figure(figsize=(6, 6))

    for segment in segments:
        plt.plot([segment.p1.x, segment.p2.x], [segment.p1.y, segment.p2.y], 'b-')

    for intersection in intersections:
        plt.plot(float(intersection.x), float(intersection.y), 'ro', label='Intersection')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Segments and Intersections')
    plt.grid(True)
    # plt.legend()
    plt.show()


def process_configuration(func, params, filename):
    segments = func(*params)  # Call the function dynamically
    intersections_d = calculate_intersections_d(segments)
    intersections_r = calculate_intersections_r(segments)
    intersections_q = calculate_intersections_q(intersections_r)

    distinct_intersection_d = set(intersections_d)
    distinct_intersection_r = set(intersections_r)
    distinct_intersection_q = set(intersections_q)

    save_segments_to_csv(segments, str(len(intersections_d)) + "-" + str(len(distinct_intersection_d)) + "-" + str(len(intersections_r)) + "-" + str(len(distinct_intersection_r)) + "-" + str(len(distinct_intersection_q)) + "_" + filename)

    if filename.startswith(("accuracy_", "rounding_", "star_intersections_7_", "star_intersections_8_")): # "parallel_", "length_", "star_",
        # accuracies = accurate_intersections(segments)
        save_accuracy_to_csv(intersections_d, intersections_r, filename)

    print("done: " + filename)


def main():
    configurations = [
        (parallel_and_collinear_1, (), "parallel_and_collinear_1.csv"),
        (parallel_and_collinear_2, (), "parallel_and_collinear_2.csv"),
        (parallel_and_collinear_3, (), "parallel_and_collinear_3.csv"),
        (parallel_and_collinear_4, (), "parallel_and_collinear_4.csv"),
        (parallel_and_collinear_5, (), "parallel_and_collinear_5.csv"),
        (parallel_and_collinear_6, (), "parallel_and_collinear_6.csv"),
        (parallel_and_collinear_7, (), "parallel_and_collinear_7.csv"),
        (parallel_and_collinear_8, (), "parallel_and_collinear_8.csv"),
        (parallel_and_collinear_9, (), "parallel_and_collinear_9.csv"),
        (parallel_and_collinear_10, (), "parallel_and_collinear_10.csv"),
        (parallel_and_collinear_11, (), "parallel_and_collinear_11.csv"),
        (parallel_and_collinear_12, (), "parallel_and_collinear_12.csv"),
        (parallel_and_collinear_13, (), "parallel_and_collinear_13.csv"),
        (parallel_and_collinear_14, (), "parallel_and_collinear_14.csv"),
        (parallel_and_collinear_15, (), "parallel_and_collinear_15.csv"),
        (parallel_and_collinear_16, (), "parallel_and_collinear_16.csv"),
        (parallel_and_collinear_17, (), "parallel_and_collinear_17.csv"),
        (parallel_and_collinear_18, (), "parallel_and_collinear_18.csv"),
        (parallel_and_collinear_19, (), "parallel_and_collinear_19.csv"),
        (parallel_and_collinear_20, (), "parallel_and_collinear_20.csv"),
        (length_0_1, (), "length_0_1.csv"),
        (length_0_2, (), "length_0_2.csv"),
        (length_0_3, (), "length_0_3.csv"),
        (length_0_4, (), "length_0_4.csv"),
        (multi_axis_1, (), "multi_axis_1.csv"),
        (multi_axis_2, (), "multi_axis_2.csv"),
        (multi_axis_3, (), "multi_axis_3.csv"),
        (multi_axis_4, (), "multi_axis_4.csv"),
        (multi_axis_5, (), "multi_axis_5.csv"),
        (multi_axis_6, (), "multi_axis_6.csv"),
        (multi_axis_7, (), "multi_axis_7.csv"),
        (multi_axis_8, (), "multi_axis_8.csv"),
        (star_intersections_1, (), "star_intersections_1.csv"),
        (star_intersections_2, (), "star_intersections_2.csv"),
        (star_intersections_3, (), "star_intersections_3.csv"),
        (star_intersections_5, (), "star_intersections_5.csv"),
        (accuracy_1, (), "accuracy_1.csv"),
        (accuracy_2, (), "accuracy_2.csv"),
        (accuracy_3, (), "accuracy_3.csv"),
        (accuracy_4, (), "accuracy_4.csv"),
        (accuracy_5, (), "accuracy_5.csv"),
        (accuracy_6, (), "accuracy_6.csv"),
        (accuracy_7, (), "accuracy_7.csv"),
        (accuracy_8, (), "accuracy_8.csv"),
        (accuracy_9, (), "accuracy_9.csv"),
        (accuracy_10, (), "accuracy_10.csv"),
        # Special star_intersections_4 with extra arguments
        #(star_intersections_4, (500, 10000), "star_intersections_4_s_500.csv"),
        (star_intersections_4, (1000, 10000), "star_intersections_4_s_1000.csv"),
        #(star_intersections_4, (1500, 10000), "star_intersections_4_s_1500.csv"),
        (star_intersections_4, (2000, 10000), "star_intersections_4_s_2000.csv"),
        #(star_intersections_4, (2500, 10000), "star_intersections_4_s_2500.csv"),
        (star_intersections_4, (3000, 10000), "star_intersections_4_s_3000.csv"),
        #(star_intersections_4, (3500, 10000), "star_intersections_4_s_3500.csv"),
        (star_intersections_4, (4000, 10000), "star_intersections_4_s_4000.csv"),
        #(star_intersections_4, (4500, 10000), "star_intersections_4_s_4500.csv"),
        (star_intersections_4, (5000, 10000), "star_intersections_4_s_5000.csv"),
        #(star_intersections_4, (5500, 10000), "star_intersections_4_s_5500.csv"),
        #(star_intersections_4, (6000, 10000), "star_intersections_4_s_6000.csv"),
        #(star_intersections_4, (6500, 10000), "star_intersections_4_s_6500.csv"),
        #(star_intersections_4, (7000, 10000), "star_intersections_4_s_7000.csv"),
        #(star_intersections_4, (7500, 10000), "star_intersections_4_s_7500.csv"),
        # (star_intersections_4, (8000, 10000), "star_intersections_4_s_8000.csv"),
        # (star_intersections_4, (8500, 10000), "star_intersections_4_s_8500.csv"),
        # (star_intersections_4, (9000, 10000), "star_intersections_4_s_9000.csv"),
        # (star_intersections_4, (9500, 10000), "star_intersections_4_s_9500.csv"),
        # (star_intersections_4, (10000, 10000), "star_intersections_4_s_10000.csv"),

        #(star_intersections_6, (500, 10000), "star_intersections_6_s_500.csv"),
        (star_intersections_6, (1000, 10000), "star_intersections_6_s_1000.csv"),
        #(star_intersections_6, (1500, 10000), "star_intersections_6_s_1500.csv"),
        (star_intersections_6, (2000, 10000), "star_intersections_6_s_2000.csv"),
        #(star_intersections_6, (2500, 10000), "star_intersections_6_s_2500.csv"),
        (star_intersections_6, (3000, 10000), "star_intersections_6_s_3000.csv"),
        #(star_intersections_6, (3500, 10000), "star_intersections_6_s_3500.csv"),
        (star_intersections_6, (4000, 10000), "star_intersections_6_s_4000.csv"),
        #(star_intersections_6, (4500, 10000), "star_intersections_6_s_4500.csv"),
        (star_intersections_6, (5000, 10000), "star_intersections_6_s_5000.csv"),
        #(star_intersections_6, (5500, 10000), "star_intersections_6_s_5500.csv"),
        #(star_intersections_6, (6000, 10000), "star_intersections_6_s_6000.csv"),
        #(star_intersections_6, (6500, 10000), "star_intersections_6_s_6500.csv"),
        #(star_intersections_6, (7000, 10000), "star_intersections_6_s_7000.csv"),
        #(star_intersections_6, (7500, 10000), "star_intersections_6_s_7500.csv"),
        # (star_intersections_6, (8000, 10000), "star_intersections_6_s_8000.csv"),
        # (star_intersections_6, (8500, 10000), "star_intersections_6_s_8500.csv"),
        # (star_intersections_6, (9000, 10000), "star_intersections_6_s_9000.csv"),
        # (star_intersections_6, (9500, 10000), "star_intersections_6_s_9500.csv"),
        # (star_intersections_6, (10000, 10000), "star_intersections_6_s_10000.csv"),

        #(star_intersections_7, (500, 10000), "star_intersections_7_s_500.csv"),
        (star_intersections_7, (1000, 10000), "star_intersections_7_s_1000.csv"),
        #(star_intersections_7, (1500, 10000), "star_intersections_7_s_1500.csv"),
        (star_intersections_7, (2000, 10000), "star_intersections_7_s_2000.csv"),
        #(star_intersections_7, (2500, 10000), "star_intersections_7_s_2500.csv"),
        (star_intersections_7, (3000, 10000), "star_intersections_7_s_3000.csv"),
        #(star_intersections_7, (3500, 10000), "star_intersections_7_s_3500.csv"),
        (star_intersections_7, (4000, 10000), "star_intersections_7_s_4000.csv"),
        #(star_intersections_7, (4500, 10000), "star_intersections_7_s_4500.csv"),
        (star_intersections_7, (5000, 10000), "star_intersections_7_s_5000.csv"),
        #(star_intersections_7, (5500, 10000), "star_intersections_7_s_5500.csv"),
        #(star_intersections_7, (6000, 10000), "star_intersections_7_s_6000.csv"),
        #(star_intersections_7, (6500, 10000), "star_intersections_7_s_6500.csv"),
        #(star_intersections_7, (7000, 10000), "star_intersections_7_s_7000.csv"),
        #(star_intersections_7, (7500, 10000), "star_intersections_7_s_7500.csv"),
        # (star_intersections_7, (8000, 10000), "star_intersections_7_s_8000.csv"),
        # (star_intersections_7, (8500, 10000), "star_intersections_7_s_8500.csv"),
        # (star_intersections_7, (9000, 10000), "star_intersections_7_s_9000.csv"),
        # (star_intersections_7, (9500, 10000), "star_intersections_7_s_9500.csv"),
        # (star_intersections_7, (10000, 10000), "star_intersections_7_s_10000.csv"),

        #(star_intersections_8, (500, 10000), "star_intersections_8_s_500.csv"),
        (star_intersections_8, (1000, 10000), "star_intersections_8_s_1000.csv"),
        #(star_intersections_8, (1500, 10000), "star_intersections_8_s_1500.csv"),
        (star_intersections_8, (2000, 10000), "star_intersections_8_s_2000.csv"),
        #(star_intersections_8, (2500, 10000), "star_intersections_8_s_2500.csv"),
        (star_intersections_8, (3000, 10000), "star_intersections_8_s_3000.csv"),
        #(star_intersections_8, (3500, 10000), "star_intersections_8_s_3500.csv"),
        (star_intersections_8, (4000, 10000), "star_intersections_8_s_4000.csv"),
        #(star_intersections_8, (4500, 10000), "star_intersections_8_s_4500.csv"),
        (star_intersections_8, (5000, 10000), "star_intersections_8_s_5000.csv"),
        #(star_intersections_8, (5500, 10000), "star_intersections_8_s_5500.csv"),
        #(star_intersections_8, (6000, 10000), "star_intersections_8_s_6000.csv"),
        #(star_intersections_8, (6500, 10000), "star_intersections_8_s_6500.csv"),
        #(star_intersections_8, (7000, 10000), "star_intersections_8_s_7000.csv"),
        #(star_intersections_8, (7500, 10000), "star_intersections_8_s_7500.csv"),
        # (star_intersections_8, (8000, 10000), "star_intersections_8_s_8000.csv"),
        # (star_intersections_8, (8500, 10000), "star_intersections_8_s_8500.csv"),
        # (star_intersections_8, (9000, 10000), "star_intersections_8_s_9000.csv"),
        # (star_intersections_8, (9500, 10000), "star_intersections_8_s_9500.csv"),
        # (star_intersections_8, (10000, 10000), "star_intersections_8_s_10000.csv"),

        #(star_intersections_4, (500, 1234567890), "star_intersections_4_m_500.csv"),
        (star_intersections_4, (1000, 1234567890), "star_intersections_4_m_1000.csv"),
        #(star_intersections_4, (1500, 1234567890), "star_intersections_4_m_1500.csv"),
        (star_intersections_4, (2000, 1234567890), "star_intersections_4_m_2000.csv"),
        #(star_intersections_4, (2500, 1234567890), "star_intersections_4_m_2500.csv"),
        (star_intersections_4, (3000, 1234567890), "star_intersections_4_m_3000.csv"),
        #(star_intersections_4, (3500, 1234567890), "star_intersections_4_m_3500.csv"),
        (star_intersections_4, (4000, 1234567890), "star_intersections_4_m_4000.csv"),
        #(star_intersections_4, (4500, 1234567890), "star_intersections_4_m_4500.csv"),
        (star_intersections_4, (5000, 1234567890), "star_intersections_4_m_5000.csv"),
        #(star_intersections_4, (5500, 1234567890), "star_intersections_4_m_5500.csv"),
        #(star_intersections_4, (6000, 1234567890), "star_intersections_4_m_6000.csv"),
        #(star_intersections_4, (6500, 1234567890), "star_intersections_4_m_6500.csv"),
        #(star_intersections_4, (7000, 1234567890), "star_intersections_4_m_7000.csv"),
        #(star_intersections_4, (7500, 1234567890), "star_intersections_4_m_7500.csv"),
        # (star_intersections_4, (8000, 1234567890), "star_intersections_4_m_8000.csv"),
        # (star_intersections_4, (8500, 1234567890), "star_intersections_4_m_8500.csv"),
        # (star_intersections_4, (9000, 1234567890), "star_intersections_4_m_9000.csv"),
        # (star_intersections_4, (9500, 1234567890), "star_intersections_4_m_9500.csv"),
        # (star_intersections_4, (10000, 1234567890), "star_intersections_4_m_10000.csv"),

        #(star_intersections_6, (500, 1234567890), "star_intersections_6_m_500.csv"),
        (star_intersections_6, (1000, 1234567890), "star_intersections_6_m_1000.csv"),
        #(star_intersections_6, (1500, 1234567890), "star_intersections_6_m_1500.csv"),
        (star_intersections_6, (2000, 1234567890), "star_intersections_6_m_2000.csv"),
        #(star_intersections_6, (2500, 1234567890), "star_intersections_6_m_2500.csv"),
        (star_intersections_6, (3000, 1234567890), "star_intersections_6_m_3000.csv"),
        #(star_intersections_6, (3500, 1234567890), "star_intersections_6_m_3500.csv"),
        (star_intersections_6, (4000, 1234567890), "star_intersections_6_m_4000.csv"),
        #(star_intersections_6, (4500, 1234567890), "star_intersections_6_m_4500.csv"),
        (star_intersections_6, (5000, 1234567890), "star_intersections_6_m_5000.csv"),
        #(star_intersections_6, (5500, 1234567890), "star_intersections_6_m_5500.csv"),
        #(star_intersections_6, (6000, 1234567890), "star_intersections_6_m_6000.csv"),
        #(star_intersections_6, (6500, 1234567890), "star_intersections_6_m_6500.csv"),
        #(star_intersections_6, (7000, 1234567890), "star_intersections_6_m_7000.csv"),
        #(star_intersections_6, (7500, 1234567890), "star_intersections_6_m_7500.csv"),
        # (star_intersections_6, (8000, 1234567890), "star_intersections_6_m_8000.csv"),
        # (star_intersections_6, (8500, 1234567890), "star_intersections_6_m_8500.csv"),
        # (star_intersections_6, (9000, 1234567890), "star_intersections_6_m_9000.csv"),
        # (star_intersections_6, (9500, 1234567890), "star_intersections_6_m_9500.csv"),
        # (star_intersections_6, (10000, 1234567890), "star_intersections_6_m_10000.csv"),

        #(star_intersections_7, (500, 1234567890), "star_intersections_7_m_500.csv"),
        (star_intersections_7, (1000, 1234567890), "star_intersections_7_m_1000.csv"),
        #(star_intersections_7, (1500, 1234567890), "star_intersections_7_m_1500.csv"),
        (star_intersections_7, (2000, 1234567890), "star_intersections_7_m_2000.csv"),
        #(star_intersections_7, (2500, 1234567890), "star_intersections_7_m_2500.csv"),
        (star_intersections_7, (3000, 1234567890), "star_intersections_7_m_3000.csv"),
        #(star_intersections_7, (3500, 1234567890), "star_intersections_7_m_3500.csv"),
        (star_intersections_7, (4000, 1234567890), "star_intersections_7_m_4000.csv"),
        #(star_intersections_7, (4500, 1234567890), "star_intersections_7_m_4500.csv"),
        (star_intersections_7, (5000, 1234567890), "star_intersections_7_m_5000.csv"),
        #(star_intersections_7, (5500, 1234567890), "star_intersections_7_m_5500.csv"),
        #(star_intersections_7, (6000, 1234567890), "star_intersections_7_m_6000.csv"),
        #(star_intersections_7, (6500, 1234567890), "star_intersections_7_m_6500.csv"),
        #(star_intersections_7, (7000, 1234567890), "star_intersections_7_m_7000.csv"),
        #(star_intersections_7, (7500, 1234567890), "star_intersections_7_m_7500.csv"),
        # (star_intersections_7, (8000, 1234567890), "star_intersections_7_m_8000.csv"),
        # (star_intersections_7, (8500, 1234567890), "star_intersections_7_m_8500.csv"),
        # (star_intersections_7, (9000, 1234567890), "star_intersections_7_m_9000.csv"),
        # (star_intersections_7, (9500, 1234567890), "star_intersections_7_m_9500.csv"),
        # (star_intersections_7, (10000, 1234567890), "star_intersections_7_m_10000.csv"),

        #(star_intersections_8, (500, 1234567890), "star_intersections_8_m_500.csv"),
        (star_intersections_8, (1000, 1234567890), "star_intersections_8_m_1000.csv"),
        #(star_intersections_8, (1500, 1234567890), "star_intersections_8_m_1500.csv"),
        (star_intersections_8, (2000, 1234567890), "star_intersections_8_m_2000.csv"),
        #(star_intersections_8, (2500, 1234567890), "star_intersections_8_m_2500.csv"),
        (star_intersections_8, (3000, 1234567890), "star_intersections_8_m_3000.csv"),
        #(star_intersections_8, (3500, 1234567890), "star_intersections_8_m_3500.csv"),
        (star_intersections_8, (4000, 1234567890), "star_intersections_8_m_4000.csv"),
        #(star_intersections_8, (4500, 1234567890), "star_intersections_8_m_4500.csv"),
        (star_intersections_8, (5000, 1234567890), "star_intersections_8_m_5000.csv"),
        #(star_intersections_8, (5500, 1234567890), "star_intersections_8_m_5500.csv"),
        #(star_intersections_8, (6000, 1234567890), "star_intersections_8_m_6000.csv"),
        #(star_intersections_8, (6500, 1234567890), "star_intersections_8_m_6500.csv"),
        #(star_intersections_8, (7000, 1234567890), "star_intersections_8_m_7000.csv"),
        #(star_intersections_8, (7500, 1234567890), "star_intersections_8_m_7500.csv"),
        # (star_intersections_8, (8000, 1234567890), "star_intersections_8_m_8000.csv"),
        # (star_intersections_8, (8500, 1234567890), "star_intersections_8_m_8500.csv"),
        # (star_intersections_8, (9000, 1234567890), "star_intersections_8_m_9000.csv"),
        # (star_intersections_8, (9500, 1234567890), "star_intersections_8_m_9500.csv"),
        # (star_intersections_8, (10000, 1234567890), "star_intersections_8_m_10000.csv"),

        #(star_intersections_4, (500, 12345678901234567890), "star_intersections_4_l_500.csv"),
        (star_intersections_4, (1000, 12345678901234567890), "star_intersections_4_l_1000.csv"),
        #(star_intersections_4, (1500, 12345678901234567890), "star_intersections_4_l_1500.csv"),
        (star_intersections_4, (2000, 12345678901234567890), "star_intersections_4_l_2000.csv"),
        #(star_intersections_4, (2500, 12345678901234567890), "star_intersections_4_l_2500.csv"),
        (star_intersections_4, (3000, 12345678901234567890), "star_intersections_4_l_3000.csv"),
        #(star_intersections_4, (3500, 12345678901234567890), "star_intersections_4_l_3500.csv"),
        (star_intersections_4, (4000, 12345678901234567890), "star_intersections_4_l_4000.csv"),
        #(star_intersections_4, (4500, 12345678901234567890), "star_intersections_4_l_4500.csv"),
        (star_intersections_4, (5000, 12345678901234567890), "star_intersections_4_l_5000.csv"),
        #(star_intersections_4, (5500, 12345678901234567890), "star_intersections_4_l_5500.csv"),
        #(star_intersections_4, (6000, 12345678901234567890), "star_intersections_4_l_6000.csv"),
        #(star_intersections_4, (6500, 12345678901234567890), "star_intersections_4_l_6500.csv"),
        #(star_intersections_4, (7000, 12345678901234567890), "star_intersections_4_l_7000.csv"),
        #(star_intersections_4, (7500, 12345678901234567890), "star_intersections_4_l_7500.csv"),
        # (star_intersections_4, (8000, 12345678901234567890), "star_intersections_4_l_8000.csv"),
        # (star_intersections_4, (8500, 12345678901234567890), "star_intersections_4_l_8500.csv"),
        # (star_intersections_4, (9000, 12345678901234567890), "star_intersections_4_l_9000.csv"),
        # (star_intersections_4, (9500, 12345678901234567890), "star_intersections_4_l_9500.csv"),
        # (star_intersections_4, (10000, 12345678901234567890), "star_intersections_4_l_10000.csv"),

        #(star_intersections_6, (500, 12345678901234567890), "star_intersections_6_l_500.csv"),
        (star_intersections_6, (1000, 12345678901234567890), "star_intersections_6_l_1000.csv"),
        #(star_intersections_6, (1500, 12345678901234567890), "star_intersections_6_l_1500.csv"),
        (star_intersections_6, (2000, 12345678901234567890), "star_intersections_6_l_2000.csv"),
        #(star_intersections_6, (2500, 12345678901234567890), "star_intersections_6_l_2500.csv"),
        (star_intersections_6, (3000, 12345678901234567890), "star_intersections_6_l_3000.csv"),
        #(star_intersections_6, (3500, 12345678901234567890), "star_intersections_6_l_3500.csv"),
        (star_intersections_6, (4000, 12345678901234567890), "star_intersections_6_l_4000.csv"),
        #(star_intersections_6, (4500, 12345678901234567890), "star_intersections_6_l_4500.csv"),
        (star_intersections_6, (5000, 12345678901234567890), "star_intersections_6_l_5000.csv"),
        #(star_intersections_6, (5500, 12345678901234567890), "star_intersections_6_l_5500.csv"),
        #(star_intersections_6, (6000, 12345678901234567890), "star_intersections_6_l_6000.csv"),
        #(star_intersections_6, (6500, 12345678901234567890), "star_intersections_6_l_6500.csv"),
        #(star_intersections_6, (7000, 12345678901234567890), "star_intersections_6_l_7000.csv"),
        #(star_intersections_6, (7500, 12345678901234567890), "star_intersections_6_l_7500.csv"),
        # (star_intersections_6, (8000, 12345678901234567890), "star_intersections_6_l_8000.csv"),
        # (star_intersections_6, (8500, 12345678901234567890), "star_intersections_6_l_8500.csv"),
        # (star_intersections_6, (9000, 12345678901234567890), "star_intersections_6_l_9000.csv"),
        # (star_intersections_6, (9500, 12345678901234567890), "star_intersections_6_l_9500.csv"),
        # (star_intersections_6, (10000, 12345678901234567890), "star_intersections_6_l_10000.csv"),

        #(star_intersections_7, (500, 12345678901234567890), "star_intersections_7_l_500.csv"),
        (star_intersections_7, (1000, 12345678901234567890), "star_intersections_7_l_1000.csv"),
        #(star_intersections_7, (1500, 12345678901234567890), "star_intersections_7_l_1500.csv"),
        (star_intersections_7, (2000, 12345678901234567890), "star_intersections_7_l_2000.csv"),
        #(star_intersections_7, (2500, 12345678901234567890), "star_intersections_7_l_2500.csv"),
        (star_intersections_7, (3000, 12345678901234567890), "star_intersections_7_l_3000.csv"),
        #(star_intersections_7, (3500, 12345678901234567890), "star_intersections_7_l_3500.csv"),
        (star_intersections_7, (4000, 12345678901234567890), "star_intersections_7_l_4000.csv"),
        #(star_intersections_7, (4500, 12345678901234567890), "star_intersections_7_l_4500.csv"),
        (star_intersections_7, (5000, 12345678901234567890), "star_intersections_7_l_5000.csv"),
        #(star_intersections_7, (5500, 12345678901234567890), "star_intersections_7_l_5500.csv"),
        #(star_intersections_7, (6000, 12345678901234567890), "star_intersections_7_l_6000.csv"),
        #(star_intersections_7, (6500, 12345678901234567890), "star_intersections_7_l_6500.csv"),
        #(star_intersections_7, (7000, 12345678901234567890), "star_intersections_7_l_7000.csv"),
        #(star_intersections_7, (7500, 12345678901234567890), "star_intersections_7_l_7500.csv"),
        # (star_intersections_7, (8000, 12345678901234567890), "star_intersections_7_l_8000.csv"),
        # (star_intersections_7, (8500, 12345678901234567890), "star_intersections_7_l_8500.csv"),
        # (star_intersections_7, (9000, 12345678901234567890), "star_intersections_7_l_9000.csv"),
        # (star_intersections_7, (9500, 12345678901234567890), "star_intersections_7_l_9500.csv"),
        # (star_intersections_7, (10000, 12345678901234567890), "star_intersections_7_l_10000.csv"),

        #(star_intersections_8, (500, 12345678901234567890), "star_intersections_8_l_500.csv"),
        (star_intersections_8, (1000, 12345678901234567890), "star_intersections_8_l_1000.csv"),
        #(star_intersections_8, (1500, 12345678901234567890), "star_intersections_8_l_1500.csv"),
        (star_intersections_8, (2000, 12345678901234567890), "star_intersections_8_l_2000.csv"),
        #(star_intersections_8, (2500, 12345678901234567890), "star_intersections_8_l_2500.csv"),
        (star_intersections_8, (3000, 12345678901234567890), "star_intersections_8_l_3000.csv"),
        #(star_intersections_8, (3500, 12345678901234567890), "star_intersections_8_l_3500.csv"),
        (star_intersections_8, (4000, 12345678901234567890), "star_intersections_8_l_4000.csv"),
        #(star_intersections_8, (4500, 12345678901234567890), "star_intersections_8_l_4500.csv"),
        (star_intersections_8, (5000, 12345678901234567890), "star_intersections_8_l_5000.csv"),
        #(star_intersections_8, (5500, 12345678901234567890), "star_intersections_8_l_5500.csv"),
        #(star_intersections_8, (6000, 12345678901234567890), "star_intersections_8_l_6000.csv"),
        #(star_intersections_8, (6500, 12345678901234567890), "star_intersections_8_l_6500.csv"),
        #(star_intersections_8, (7000, 12345678901234567890), "star_intersections_8_l_7000.csv"),
        #(star_intersections_8, (7500, 12345678901234567890), "star_intersections_8_l_7500.csv"),
        # (star_intersections_8, (8000, 12345678901234567890), "star_intersections_8_l_8000.csv"),
        # (star_intersections_8, (8500, 12345678901234567890), "star_intersections_8_l_8500.csv"),
        # (star_intersections_8, (9000, 12345678901234567890), "star_intersections_8_l_9000.csv"),
        # (star_intersections_8, (9500, 12345678901234567890), "star_intersections_8_l_9500.csv"),
        # (star_intersections_8, (10000, 12345678901234567890), "star_intersections_8_l_10000.csv"),

        # Random_x calls
        # (random_x, (500, 10000), "random_s_500.csv"),
        (random_x, (1000, 10000), "random_s_1000.csv"),
        # (random_x, (1500, 10000), "random_s_1500.csv"),
        (random_x, (2000, 10000), "random_s_2000.csv"),
        # (random_x, (2500, 10000), "random_s_2500.csv"),
        (random_x, (3000, 10000), "random_s_3000.csv"),
        # (random_x, (3500, 10000), "random_s_3500.csv"),
        (random_x, (4000, 10000), "random_s_4000.csv"),
        # (random_x, (4500, 10000), "random_s_4500.csv"),
        (random_x, (5000, 10000), "random_s_5000.csv"),
        # (random_x, (5500, 10000), "random_s_5500.csv"),
        # (random_x, (6000, 10000), "random_s_6000.csv"),
        # (random_x, (6500, 10000), "random_s_6500.csv"),
        # (random_x, (7000, 10000), "random_s_7000.csv"),
        # (random_x, (7500, 10000), "random_s_7500.csv"),
        # (random_x, (8000, 10000), "random_s_8000.csv"),
        # (random_x, (8500, 10000), "random_s_8500.csv"),
        # (random_x, (9000, 10000), "random_s_9000.csv"),
        # (random_x, (9500, 10000), "random_s_9500.csv"),
        # (random_x, (10000, 10000), "random_s_10000.csv"),

        # (random_x, (500, 1234567890), "random_m_500.csv"),
        (random_x, (1000, 1234567890), "random_m_1000.csv"),
        # (random_x, (1500, 1234567890), "random_m_1500.csv"),
        (random_x, (2000, 1234567890), "random_m_2000.csv"),
        # (random_x, (2500, 1234567890), "random_m_2500.csv"),
        (random_x, (3000, 1234567890), "random_m_3000.csv"),
        # (random_x, (3500, 1234567890), "random_m_3500.csv"),
        (random_x, (4000, 1234567890), "random_m_4000.csv"),
        # (random_x, (4500, 1234567890), "random_m_4500.csv"),
        (random_x, (5000, 1234567890), "random_m_5000.csv"),
        # (random_x, (5500, 1234567890), "random_m_5500.csv"),
        # (random_x, (6000, 1234567890), "random_m_6000.csv"),
        # (random_x, (6500, 1234567890), "random_m_6500.csv"),
        # (random_x, (7000, 1234567890), "random_m_7000.csv"),
        # (random_x, (7500, 1234567890), "random_m_7500.csv"),
        # (random_x, (8000, 1234567890), "random_m_8000.csv"),
        # (random_x, (8500, 1234567890), "random_m_8500.csv"),
        # (random_x, (9000, 1234567890), "random_m_9000.csv"),
        # (random_x, (9500, 1234567890), "random_m_9500.csv"),
        # (random_x, (10000, 1234567890), "random_m_10000.csv"),

        # (random_x, (500, 12345678901234567890), "random_l_500.csv"),
        (random_x, (1000, 12345678901234567890), "random_l_1000.csv"),
        # (random_x, (1500, 12345678901234567890), "random_l_1500.csv"),
        (random_x, (2000, 12345678901234567890), "random_l_2000.csv"),
        # (random_x, (2500, 12345678901234567890), "random_l_2500.csv"),
        (random_x, (3000, 12345678901234567890), "random_l_3000.csv"),
        # (random_x, (3500, 12345678901234567890), "random_l_3500.csv"),
        (random_x, (4000, 12345678901234567890), "random_l_4000.csv"),
        # (random_x, (4500, 12345678901234567890), "random_l_4500.csv"),
        (random_x, (5000, 12345678901234567890), "random_l_5000.csv"),
        # (random_x, (5500, 12345678901234567890), "random_l_5500.csv"),
        # (random_x, (6000, 12345678901234567890), "random_l_6000.csv"),
        # (random_x, (6500, 12345678901234567890), "random_l_6500.csv"),
        # (random_x, (7000, 12345678901234567890), "random_l_7000.csv"),
        # (random_x, (7500, 12345678901234567890), "random_l_7500.csv"),
        # (random_x, (8000, 12345678901234567890), "random_l_8000.csv"),
        # (random_x, (8500, 12345678901234567890), "random_l_8500.csv"),
        # (random_x, (9000, 12345678901234567890), "random_l_9000.csv"),
        # (random_x, (9500, 12345678901234567890), "random_l_9500.csv"),
        # (random_x, (10000, 12345678901234567890), "random_l_10000.csv"),

        # Clustered_x calls
        # (clustered_x, (500, 5000, 1), "clustered_s_1.csv"),
        (clustered_x, (1000, 10000, 1), "clustered_m_1.csv"),
        # (clustered_x, (1500, 15000, 1), "clustered_l_1.csv"),
        (clustered_x, (2000, 20000, 1), "clustered_xl_1.csv"),
        # (clustered_x, (2500, 25000, 1), "clustered_xxl_1.csv"),
        (clustered_x, (3000, 30000, 1), "clustered_xxxl_1.csv"),
        # (clustered_x, (3500, 35000, 1), "clustered_xxxxl_1.csv"),
        (clustered_x, (4000, 40000, 1), "clustered_xxxxxl_1.csv"),
        # (clustered_x, (4500, 45000, 1), "clustered_xxxxxxl_1.csv"),
        (clustered_x, (5000, 50000, 1), "clustered_xxxxxxxl_1.csv"),
        # (clustered_x, (5500, 55000, 1), "clustered_xxxxxxxxl_1.csv"),
        # (clustered_x, (6000, 60000, 1), "clustered_xxxxxxxxxl_1.csv"),
        # (clustered_x, (6500, 65000, 1), "clustered_xxxxxxxxxxl_1.csv"),
        # (clustered_x, (7000, 70000, 1), "clustered_xxxxxxxxxxxl_1.csv"),
        # (clustered_x, (7500, 75000, 1), "clustered_xxxxxxxxxxxxl_1.csv"),
        # (clustered_x, (8000, 80000, 1), "clustered_xxxxxxxxxxxxxl_1.csv"),
        # (clustered_x, (8500, 85000, 1), "clustered_xxxxxxxxxxxxxxxl_1.csv"),
        # (clustered_x, (9000, 90000, 1), "clustered_xxxxxxxxxxxxxxxxxl_1.csv"),
        # (clustered_x, (9500, 95000, 1), "clustered_xxxxxxxxxxxxxxxxxxl_1.csv"),
        # (clustered_x, (10000, 100000, 1), "clustered_xxxxxxxxxxxxxxxxxxxl_1.csv"),

        # Clustered_x calls
        # (clustered_x, (500, 5000, 2), "clustered_s_2.csv"),
        # (clustered_x, (1000, 10000, 2), "clustered_m_2.csv"),
        # (clustered_x, (1500, 15000, 2), "clustered_l_2.csv"),
        # (clustered_x, (2000, 20000, 2), "clustered_xl_2.csv"),
        # (clustered_x, (2500, 25000, 2), "clustered_xxl_2.csv"),
        # (clustered_x, (3000, 30000, 2), "clustered_xxxl_2.csv"),
        # (clustered_x, (3500, 35000, 2), "clustered_xxxxl_2.csv"),
        # (clustered_x, (4000, 40000, 2), "clustered_xxxxxl_2.csv"),
        # (clustered_x, (4500, 45000, 2), "clustered_xxxxxxl_2.csv"),
        # (clustered_x, (5000, 50000, 2), "clustered_xxxxxxxl_2.csv"),
        # (clustered_x, (5500, 55000, 2), "clustered_xxxxxxxxl_2.csv"),
        # (clustered_x, (6000, 60000, 2), "clustered_xxxxxxxxxl_2.csv"),
        # (clustered_x, (6500, 65000, 2), "clustered_xxxxxxxxxxl_2.csv"),
        # (clustered_x, (7000, 70000, 2), "clustered_xxxxxxxxxxxl_2.csv"),
        # (clustered_x, (7500, 75000, 2), "clustered_xxxxxxxxxxxxl_2.csv"),
        # (clustered_x, (8000, 80000, 2), "clustered_xxxxxxxxxxxxxl_2.csv"),
        # (clustered_x, (8500, 85000, 2), "clustered_xxxxxxxxxxxxxxxl_2.csv"),
        # (clustered_x, (9000, 90000, 2), "clustered_xxxxxxxxxxxxxxxxxl_2.csv"),
        # (clustered_x, (9500, 95000, 2), "clustered_xxxxxxxxxxxxxxxxxxl_2.csv"),
        # (clustered_x, (10000, 100000, 2), "clustered_xxxxxxxxxxxxxxxxxxxl_2.csv"),

        # Clustered_x calls
        # (clustered_x, (500, 5000, 3), "clustered_s_3.csv"),
        # (clustered_x, (1000, 10000, 3), "clustered_m_3.csv"),
        # (clustered_x, (1500, 15000, 3), "clustered_l_3.csv"),
        # (clustered_x, (2000, 20000, 3), "clustered_xl_3.csv"),
        # (clustered_x, (2500, 25000, 3), "clustered_xxl_3.csv"),
        # (clustered_x, (3000, 30000, 3), "clustered_xxxl_3.csv"),
        # (clustered_x, (3500, 35000, 3), "clustered_xxxxl_3.csv"),
        # (clustered_x, (4000, 40000, 3), "clustered_xxxxxl_3.csv"),
        # (clustered_x, (4500, 45000, 3), "clustered_xxxxxxl_3.csv"),
        # (clustered_x, (5000, 50000, 3), "clustered_xxxxxxxl_3.csv"),
        # (clustered_x, (5500, 55000, 3), "clustered_xxxxxxxxl_3.csv"),
        # (clustered_x, (6000, 60000, 3), "clustered_xxxxxxxxxl_3.csv"),
        # (clustered_x, (6500, 65000, 3), "clustered_xxxxxxxxxxl_3.csv"),
        # (clustered_x, (7000, 70000, 3), "clustered_xxxxxxxxxxxl_3.csv"),
        # (clustered_x, (7500, 75000, 3), "clustered_xxxxxxxxxxxxl_3.csv"),
        # (clustered_x, (8000, 80000, 3), "clustered_xxxxxxxxxxxxxl_3.csv"),
        # (clustered_x, (8500, 85000, 3), "clustered_xxxxxxxxxxxxxxxl_3.csv"),
        # (clustered_x, (9000, 90000, 3), "clustered_xxxxxxxxxxxxxxxxxl_3.csv"),
        # (clustered_x, (9500, 95000, 3), "clustered_xxxxxxxxxxxxxxxxxxl_3.csv"),
        # (clustered_x, (10000, 100000, 3), "clustered_xxxxxxxxxxxxxxxxxxxl_3.csv"),

        # Clustered_x calls
        # (clustered_x, (500, 5000, 4), "clustered_s_4.csv"),
        # (clustered_x, (1000, 10000, 4), "clustered_m_4.csv"),
        # (clustered_x, (1500, 15000, 4), "clustered_l_4.csv"),
        # (clustered_x, (2000, 20000, 4), "clustered_xl_4.csv"),
        # (clustered_x, (2500, 25000, 4), "clustered_xxl_4.csv"),
        # (clustered_x, (3000, 30000, 4), "clustered_xxxl_4.csv"),
        # (clustered_x, (3500, 35000, 4), "clustered_xxxxl_4.csv"),
        # (clustered_x, (4000, 40000, 4), "clustered_xxxxxl_4.csv"),
        # (clustered_x, (4500, 45000, 4), "clustered_xxxxxxl_4.csv"),
        # (clustered_x, (5000, 50000, 4), "clustered_xxxxxxxl_4.csv"),
        # (clustered_x, (5500, 55000, 4), "clustered_xxxxxxxxl_4.csv"),
        # (clustered_x, (6000, 60000, 4), "clustered_xxxxxxxxxl_4.csv"),
        # (clustered_x, (6500, 65000, 4), "clustered_xxxxxxxxxxl_4.csv"),
        # (clustered_x, (7000, 70000, 4), "clustered_xxxxxxxxxxxl_4.csv"),
        # (clustered_x, (7500, 75000, 4), "clustered_xxxxxxxxxxxxl_4.csv"),
        # (clustered_x, (8000, 80000, 4), "clustered_xxxxxxxxxxxxxl_4.csv"),
        # (clustered_x, (8500, 85000, 4), "clustered_xxxxxxxxxxxxxxxl_4.csv"),
        # (clustered_x, (9000, 90000, 4), "clustered_xxxxxxxxxxxxxxxxxl_4.csv"),
        # (clustered_x, (9500, 95000, 4), "clustered_xxxxxxxxxxxxxxxxxxl_4.csv"),
        # (clustered_x, (10000, 100000, 4), "clustered_xxxxxxxxxxxxxxxxxxxl_4.csv"),

        # Clustered_x calls
        # (clustered_x, (500, 5000, 5), "clustered_s_5.csv"),
        (clustered_x, (1000, 10000, 5), "clustered_m_5.csv"),
        # (clustered_x, (1500, 15000, 5), "clustered_l_5.csv"),
        (clustered_x, (2000, 20000, 5), "clustered_xl_5.csv"),
        # (clustered_x, (2500, 25000, 5), "clustered_xxl_5.csv"),
        (clustered_x, (3000, 30000, 5), "clustered_xxxl_5.csv"),
        # (clustered_x, (3500, 35000, 5), "clustered_xxxxl_5.csv"),
        (clustered_x, (4000, 40000, 5), "clustered_xxxxxl_5.csv"),
        # (clustered_x, (4500, 45000, 5), "clustered_xxxxxxl_5.csv"),
        (clustered_x, (5000, 50000, 5), "clustered_xxxxxxxl_5.csv"),
        # (clustered_x, (5500, 55000, 5), "clustered_xxxxxxxxl_5.csv"),
        # (clustered_x, (6000, 60000, 5), "clustered_xxxxxxxxxl_5.csv"),
        # (clustered_x, (6500, 65000, 5), "clustered_xxxxxxxxxxl_5.csv"),
        # (clustered_x, (7000, 70000, 5), "clustered_xxxxxxxxxxxl_5.csv"),
        # (clustered_x, (7500, 75000, 5), "clustered_xxxxxxxxxxxxl_5.csv"),
        # (clustered_x, (8000, 80000, 5), "clustered_xxxxxxxxxxxxxl_5.csv"),
        # (clustered_x, (8500, 85000, 5), "clustered_xxxxxxxxxxxxxxxl_5.csv"),
        # (clustered_x, (9000, 90000, 5), "clustered_xxxxxxxxxxxxxxxxxl_5.csv"),
        # (clustered_x, (9500, 95000, 5), "clustered_xxxxxxxxxxxxxxxxxxl_5.csv"),
        # (clustered_x, (10000, 100000, 5), "clustered_xxxxxxxxxxxxxxxxxxxl_5.csv"),

        # (clustered_x, (500, 5000, 10), "clustered_s_10.csv"),
        (clustered_x, (1000, 10000, 10), "clustered_m_10.csv"),
        # (clustered_x, (1500, 15000, 10), "clustered_l_10.csv"),
        (clustered_x, (2000, 20000, 10), "clustered_xl_10.csv"),
        # (clustered_x, (2500, 25000, 10), "clustered_xxl_10.csv"),
        (clustered_x, (3000, 30000, 10), "clustered_xxxl_10.csv"),
        # (clustered_x, (3500, 35000, 10), "clustered_xxxxl_10.csv"),
        (clustered_x, (4000, 40000, 10), "clustered_xxxxxl_10.csv"),
        # (clustered_x, (4500, 45000, 10), "clustered_xxxxxxl_10.csv"),
        (clustered_x, (5000, 50000, 10), "clustered_xxxxxxxl_10.csv"),
        # (clustered_x, (5500, 55000, 10), "clustered_xxxxxxxxl_10.csv"),
        # (clustered_x, (6000, 60000, 10), "clustered_xxxxxxxxxl_10.csv"),
        # (clustered_x, (6500, 65000, 10), "clustered_xxxxxxxxxxl_10.csv"),
        # (clustered_x, (7000, 70000, 10), "clustered_xxxxxxxxxxxl_10.csv"),
        # (clustered_x, (7500, 75000, 10), "clustered_xxxxxxxxxxxxl_10.csv"),
        # (clustered_x, (8000, 80000, 10), "clustered_xxxxxxxxxxxxxl_10.csv"),
        # (clustered_x, (8500, 85000, 10), "clustered_xxxxxxxxxxxxxxxl_10.csv"),
        # (clustered_x, (9000, 90000, 10), "clustered_xxxxxxxxxxxxxxxxxl_10.csv"),
        # (clustered_x, (9500, 95000, 10), "clustered_xxxxxxxxxxxxxxxxxxl_10.csv"),
        # (clustered_x, (10000, 100000, 10), "clustered_xxxxxxxxxxxxxxxxxxxl_10.csv"),

        # (clustered_x, (500, 5000, 20), "clustered_s_20.csv"),
        # (clustered_x, (1000, 10000, 20), "clustered_m_20.csv"),
        # (clustered_x, (1500, 15000, 20), "clustered_l_20.csv"),
        # (clustered_x, (2000, 20000, 20), "clustered_xl_20.csv"),
        # (clustered_x, (2500, 25000, 20), "clustered_xxl_20.csv"),
        # (clustered_x, (3000, 30000, 20), "clustered_xxxl_20.csv"),
        # (clustered_x, (3500, 35000, 20), "clustered_xxxxl_20.csv"),
        # (clustered_x, (4000, 40000, 20), "clustered_xxxxxl_20.csv"),
        # (clustered_x, (4500, 45000, 20), "clustered_xxxxxxl_20.csv"),
        # (clustered_x, (5000, 50000, 20), "clustered_xxxxxxxl_20.csv"),
        # (clustered_x, (5500, 55000, 20), "clustered_xxxxxxxxl_20.csv"),
        # (clustered_x, (6000, 60000, 20), "clustered_xxxxxxxxxl_20.csv"),
        # (clustered_x, (6500, 65000, 20), "clustered_xxxxxxxxxxl_20.csv"),
        # (clustered_x, (7000, 70000, 20), "clustered_xxxxxxxxxxxl_20.csv"),
        # (clustered_x, (7500, 75000, 20), "clustered_xxxxxxxxxxxxl_20.csv"),
        # (clustered_x, (8000, 80000, 20), "clustered_xxxxxxxxxxxxxl_20.csv"),
        # (clustered_x, (8500, 85000, 20), "clustered_xxxxxxxxxxxxxxxl_20.csv"),
        # (clustered_x, (9000, 90000, 20), "clustered_xxxxxxxxxxxxxxxxxl_20.csv"),
        # (clustered_x, (9500, 95000, 20), "clustered_xxxxxxxxxxxxxxxxxxl_20.csv"),
        # (clustered_x, (10000, 100000, 20), "clustered_xxxxxxxxxxxxxxxxxxxl_20.csv"),

        # (clustered_x, (500, 5000, 40), "clustered_s_40.csv"),
        # (clustered_x, (1000, 10000, 40), "clustered_m_40.csv"),
        # (clustered_x, (1500, 15000, 40), "clustered_l_40.csv"),
        # (clustered_x, (2000, 20000, 40), "clustered_xl_40.csv"),
        # (clustered_x, (2500, 25000, 40), "clustered_xxl_40.csv"),
        # (clustered_x, (3000, 30000, 40), "clustered_xxxl_40.csv"),
        # (clustered_x, (3500, 35000, 40), "clustered_xxxxl_40.csv"),
        # (clustered_x, (4000, 40000, 40), "clustered_xxxxxl_40.csv"),
        # (clustered_x, (4500, 45000, 40), "clustered_xxxxxxl_40.csv"),
        # (clustered_x, (5000, 50000, 40), "clustered_xxxxxxxl_40.csv"),
        # (clustered_x, (5500, 55000, 40), "clustered_xxxxxxxxl_40.csv"),
        # (clustered_x, (6000, 60000, 40), "clustered_xxxxxxxxxl_40.csv"),
        # (clustered_x, (6500, 65000, 40), "clustered_xxxxxxxxxxl_40.csv"),
        # (clustered_x, (7000, 70000, 40), "clustered_xxxxxxxxxxxl_40.csv"),
        # (clustered_x, (7500, 75000, 40), "clustered_xxxxxxxxxxxxl_40.csv"),
        # (clustered_x, (8000, 80000, 40), "clustered_xxxxxxxxxxxxxl_40.csv"),
        # (clustered_x, (8500, 85000, 40), "clustered_xxxxxxxxxxxxxxxl_40.csv"),
        # (clustered_x, (9000, 90000, 40), "clustered_xxxxxxxxxxxxxxxxxl_40.csv"),
        # (clustered_x, (9500, 95000, 40), "clustered_xxxxxxxxxxxxxxxxxxl_40.csv"),
        # (clustered_x, (10000, 100000, 40), "clustered_xxxxxxxxxxxxxxxxxxxl_40.csv"),

        # (clustered_x, (500, 5000, 60), "clustered_s_60.csv"),
        # (clustered_x, (1000, 10000, 60), "clustered_m_60.csv"),
        # (clustered_x, (1500, 15000, 60), "clustered_l_60.csv"),
        # (clustered_x, (2000, 20000, 60), "clustered_xl_60.csv"),
        # (clustered_x, (2500, 25000, 60), "clustered_xxl_60.csv"),
        # (clustered_x, (3000, 30000, 60), "clustered_xxxl_60.csv"),
        # (clustered_x, (3500, 35000, 60), "clustered_xxxxl_60.csv"),
        # (clustered_x, (4000, 40000, 60), "clustered_xxxxxl_60.csv"),
        # (clustered_x, (4500, 45000, 60), "clustered_xxxxxxl_60.csv"),
        # (clustered_x, (5000, 50000, 60), "clustered_xxxxxxxl_60.csv"),
        # (clustered_x, (6000, 60000, 60), "clustered_xxxxxxxxl_60.csv"),
        # (clustered_x, (6000, 60000, 60), "clustered_xxxxxxxxxl_60.csv"),
        # (clustered_x, (6500, 65000, 60), "clustered_xxxxxxxxxxl_60.csv"),
        # (clustered_x, (7000, 70000, 60), "clustered_xxxxxxxxxxxl_60.csv"),
        # (clustered_x, (7500, 75000, 60), "clustered_xxxxxxxxxxxxl_60.csv"),
        # (clustered_x, (8000, 80000, 60), "clustered_xxxxxxxxxxxxxl_60.csv"),
        # (clustered_x, (8500, 85000, 60), "clustered_xxxxxxxxxxxxxxxl_60.csv"),
        # (clustered_x, (9000, 90000, 60), "clustered_xxxxxxxxxxxxxxxxxl_60.csv"),
        # (clustered_x, (9500, 95000, 60), "clustered_xxxxxxxxxxxxxxxxxxl_60.csv"),
        # (clustered_x, (10000, 100000, 60), "clustered_xxxxxxxxxxxxxxxxxxxl_60.csv"),

        # Rounding calls
        (rounding, (500, 10000, 10000), "rounding_s_500.csv"),
        (rounding, (1000, 10000, 10000), "rounding_s_1000.csv"),
        (rounding, (1500, 10000, 10000), "rounding_s_1500.csv"),
        (rounding, (2000, 10000, 10000), "rounding_s_2000.csv"),
        (rounding, (2500, 10000, 10000), "rounding_s_2500.csv"),
        (rounding, (3000, 10000, 10000), "rounding_s_3000.csv"),
        (rounding, (3500, 10000, 10000), "rounding_s_3500.csv"),
        (rounding, (4000, 10000, 10000), "rounding_s_4000.csv"),
        (rounding, (4500, 10000, 10000), "rounding_s_4500.csv"),
        (rounding, (5000, 10000, 10000), "rounding_s_5000.csv"),
        (rounding, (5500, 10000, 10000), "rounding_s_5500.csv"),
        (rounding, (6000, 10000, 10000), "rounding_s_6000.csv"),
        (rounding, (6500, 10000, 10000), "rounding_s_6500.csv"),
        (rounding, (7000, 10000, 10000), "rounding_s_7000.csv"),
        (rounding, (7500, 10000, 10000), "rounding_s_7500.csv"),
        # (rounding, (8000, 10000, 10000), "rounding_s_8000.csv"),
        # (rounding, (8500, 10000, 10000), "rounding_s_8500.csv"),
        # (rounding, (9000, 10000, 10000), "rounding_s_9000.csv"),
        # (rounding, (9500, 10000, 10000), "rounding_s_9500.csv"),
        # (rounding, (10000, 10000, 10000), "rounding_s_10000.csv"),

        #(rounding, (500, 1234567890, 10000), "rounding_m_500.csv"),
        (rounding, (1000, 1234567890, 10000), "rounding_m_1000.csv"),
        #(rounding, (1500, 1234567890, 10000), "rounding_m_1500.csv"),
        (rounding, (2000, 1234567890, 10000), "rounding_m_2000.csv"),
        #(rounding, (2500, 1234567890, 10000), "rounding_m_2500.csv"),
        (rounding, (3000, 1234567890, 10000), "rounding_m_3000.csv"),
        #(rounding, (3500, 1234567890, 10000), "rounding_m_3500.csv"),
        (rounding, (4000, 1234567890, 10000), "rounding_m_4000.csv"),
        #(rounding, (4500, 1234567890, 10000), "rounding_m_4500.csv"),
        (rounding, (5000, 1234567890, 10000), "rounding_m_5000.csv"),
        #(rounding, (5500, 1234567890, 10000), "rounding_m_5500.csv"),
        #(rounding, (6000, 1234567890, 10000), "rounding_m_6000.csv"),
        #(rounding, (6500, 1234567890, 10000), "rounding_m_6500.csv"),
        #(rounding, (7000, 1234567890, 10000), "rounding_m_7000.csv"),
        #(rounding, (7500, 1234567890, 10000), "rounding_m_7500.csv"),
        # (rounding, (8000, 1234567890, 10000), "rounding_m_8000.csv"),
        # (rounding, (8500, 1234567890, 10000), "rounding_m_8500.csv"),
        # (rounding, (9000, 1234567890, 10000), "rounding_m_9000.csv"),
        # (rounding, (9500, 1234567890, 10000), "rounding_m_9500.csv"),
        # (rounding, (10000, 1234567890, 10000), "rounding_m_10000.csv"),

        #(rounding, (500, 12345678901234567890, 10000), "rounding_l_500.csv"),
        (rounding, (1000, 12345678901234567890, 10000), "rounding_l_1000.csv"),
        #(rounding, (1500, 12345678901234567890, 10000), "rounding_l_1500.csv"),
        (rounding, (2000, 12345678901234567890, 10000), "rounding_l_2000.csv"),
        #(rounding, (2500, 12345678901234567890, 10000), "rounding_l_2500.csv"),
        (rounding, (3000, 12345678901234567890, 10000), "rounding_l_3000.csv"),
        #(rounding, (3500, 12345678901234567890, 10000), "rounding_l_3500.csv"),
        (rounding, (4000, 12345678901234567890, 10000), "rounding_l_4000.csv"),
        #(rounding, (4500, 12345678901234567890, 10000), "rounding_l_4500.csv"),
        (rounding, (5000, 12345678901234567890, 10000), "rounding_l_5000.csv"),
        #(rounding, (5500, 12345678901234567890, 10000), "rounding_l_5500.csv"),
        #(rounding, (6000, 12345678901234567890, 10000), "rounding_l_6000.csv"),
        #(rounding, (6500, 12345678901234567890, 10000), "rounding_l_6500.csv"),
        #(rounding, (7000, 12345678901234567890, 10000), "rounding_l_7000.csv"),
        #(rounding, (7500, 12345678901234567890, 10000), "rounding_l_7500.csv"),
        # (rounding, (8000, 12345678901234567890, 10000), "rounding_l_8000.csv"),
        # (rounding, (8500, 12345678901234567890, 10000), "rounding_l_8500.csv"),
        # (rounding, (9000, 12345678901234567890, 10000), "rounding_l_9000.csv"),
        # (rounding, (9500, 12345678901234567890, 10000), "rounding_l_9500.csv"),
        # (rounding, (10000, 12345678901234567890, 10000), "rounding_l_10000.csv"),

        (star_intersections_9, (500, 250, 1234567890), "star_intersections_9_500.csv"),
        (star_intersections_9, (1000, 500, 1234567890), "star_intersections_9_1000.csv"),
        (star_intersections_9, (1500, 750, 1234567890), "star_intersections_9_1500.csv"),
        (star_intersections_9, (2000, 1000, 1234567890), "star_intersections_9_2000.csv"),
        (star_intersections_9, (2500, 1250, 1234567890), "star_intersections_9_2500.csv"),
        (star_intersections_9, (3000, 1500, 1234567890), "star_intersections_9_3000.csv"),
        (star_intersections_9, (3500, 1750, 1234567890), "star_intersections_9_3500.csv"),
        (star_intersections_9, (4000, 2000, 1234567890), "star_intersections_9_4000.csv"),
        (star_intersections_9, (4500, 2250, 1234567890), "star_intersections_9_4500.csv"),
        (star_intersections_9, (5000, 2500, 1234567890), "star_intersections_9_5000.csv"),
        (star_intersections_9, (5500, 2750, 1234567890), "star_intersections_9_5500.csv"),
        (star_intersections_9, (6000, 3000, 1234567890), "star_intersections_9_6000.csv"),
        (star_intersections_9, (6500, 3250, 1234567890), "star_intersections_9_6500.csv"),
        (star_intersections_9, (7000, 3500, 1234567890), "star_intersections_9_7000.csv"),
        (star_intersections_9, (7500, 3750, 1234567890), "star_intersections_9_7500.csv"),
        # (star_intersections_9, (8000, 4000, 1234567890), "star_intersections_9_8000.csv"),
        # (star_intersections_9, (8500, 4250, 1234567890), "star_intersections_9_8500.csv"),
        # (star_intersections_9, (9000, 4500, 1234567890), "star_intersections_9_9000.csv"),
        # (star_intersections_9, (9500, 4750, 1234567890), "star_intersections_9_9500.csv"),
        # (star_intersections_9, (10000, 5000, 1234567890), "star_intersections_9_10000.csv"),

        (star_intersections_9, (500, 1500, 1234567890), "star_intersections_10_500.csv"),
        (star_intersections_9, (1000, 3000, 1234567890), "star_intersections_10_1000.csv"),
        (star_intersections_9, (1500, 4500, 1234567890), "star_intersections_10_1500.csv"),
        (star_intersections_9, (2000, 6000, 1234567890), "star_intersections_10_2000.csv"),
        (star_intersections_9, (2500, 7500, 1234567890), "star_intersections_10_2500.csv"),
        (star_intersections_9, (3000, 9000, 1234567890), "star_intersections_10_3000.csv"),
        (star_intersections_9, (3500, 10500, 1234567890), "star_intersections_10_3500.csv"),
        (star_intersections_9, (4000, 12000, 1234567890), "star_intersections_10_4000.csv"),
        (star_intersections_9, (4500, 13500, 1234567890), "star_intersections_10_4500.csv"),
        (star_intersections_9, (5000, 15000, 1234567890), "star_intersections_10_5000.csv"),
        (star_intersections_9, (5500, 16500, 1234567890), "star_intersections_10_5500.csv"),
        (star_intersections_9, (6000, 18000, 1234567890), "star_intersections_10_6000.csv"),
        (star_intersections_9, (6500, 19500, 1234567890), "star_intersections_10_6500.csv"),
        (star_intersections_9, (7000, 21000, 1234567890), "star_intersections_10_7000.csv"),
        (star_intersections_9, (7500, 22500, 1234567890), "star_intersections_10_7500.csv"),
        # (star_intersections_9, (8000, 24000, 1234567890), "star_intersections_10_8000.csv"),
        # (star_intersections_9, (8500, 25500, 1234567890), "star_intersections_10_8500.csv"),
        # (star_intersections_9, (9000, 27000, 1234567890), "star_intersections_10_9000.csv"),
        # (star_intersections_9, (9500, 28500, 1234567890), "star_intersections_10_9500.csv"),
        # (star_intersections_9, (10000, 30000, 1234567890), "star_intersections_10_10000.csv"),
    ]

    # Parallelize the loop using ThreadPoolExecutor
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(process_configuration, func, params, filename): (func, params, filename) for func, params, filename in configurations}
        # Wait for all the tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # This will raise an exception if the task failed
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random line segments and calculate their intersections.")

    args = parser.parse_args()

    main()

