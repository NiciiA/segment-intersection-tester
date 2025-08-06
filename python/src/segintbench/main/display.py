import argparse
from fractions import Fraction

import matplotlib.pyplot as plt

from segintbench.utils import *


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
    parser.add_argument('-r', '--rational', action='store_true',
                        help='Use rational numbers (Fraction) instead of floats for coordinates.')

    args = parser.parse_args()

    # Load segments from the CSV file
    segments = list(read_segments_from_csv(args.file))

    # Calculate intersections
    if args.rational:
        intersections = list(calculate_intersections_pairwise(segments, conv=Fraction))
    else:
        intersections = list(calculate_intersections_pairwise(segments))

    plot_segments_and_intersections(segments, intersections)


if __name__ == '__main__':
    main()
