import argparse
import sys
import time

from segintbench.utils import *


def main(parse_bin, calculate_intersections, postprocess=None):
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    parser.add_argument('-f', '--file', required=True, help='Path to the CSV file')
    parser.add_argument('-a', '--accuracy', action='store_true', help='Print intersections if this flag is set')
    parser.add_argument('-e', '--echo', action='store_true', help='Print parsed coordinates for parser validation')

    args = parser.parse_args()
    filepath = args.file

    # Validate input file
    if not filepath.endswith(".csv"):
        print("Error: The specified file is not a CSV file.")
        exit(1)

    if not os.path.exists(filepath):
        print(f"Error: The file {filepath} does not exist.")
        exit(1)

    # Read and parse segments from the file
    segments = list(read_segments_from_csv(filepath, decode=parse_bin))

    if args.echo:
        write_segments_to_csv(segments, sys.stdout, False)
        return 1

    # Main execution
    initial_memory = get_memory_usage()
    start_time = time.perf_counter()

    # Calculate intersections
    intersections = list(calculate_intersections(segments))

    end_time = time.perf_counter()
    final_memory = get_memory_usage()

    execution_time = end_time - start_time
    memory_usage = final_memory - initial_memory
    execution_time_ms = int(execution_time * 1000)

    if postprocess:
        intersections = postprocess(intersections)
    total_intersections = len(intersections)

    # Output results
    if args.accuracy:
        print("p_x;p_y")
        for point in intersections:
            print(f"{point.x};{point.y}")
    else:
        print(total_intersections)
        print(execution_time_ms)
        print(memory_usage)
