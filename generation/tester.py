# python tester.py -f ./tests -a ./tests/accuracies

import concurrent.futures
import csv
import math
import os
import argparse
import re
import struct
import subprocess


def run_command(command):
    """Run a shell command and capture the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Split the output by lines and return as a list
        output_lines = result.stdout.strip().split('\n')

        # Check if the output is empty
        if not output_lines:
            print(f"Warning: No output from command {command}")
            return []

        return output_lines
    except Exception as e:
        print(f"Error running command {command}: {e}")
        return []


def bin2float(binary_string, single=False):
    if len(binary_string) != (32 if single else 64):
        raise ValueError("Binary string length must be 32 (for float) or 64 (for double).")
    byte_data = int(binary_string, 2).to_bytes(4 if single else 8, byteorder='big')
    return struct.unpack('>f' if single else '>d', byte_data)[0]


def get_files_from_argument(path):
    """Return a list of files given a file, list of files, or folder."""
    if os.path.isdir(path):
        # If it's a directory, return all files in the directory
        return [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    else:
        # If it's a single file or comma-separated list of files, return those
        return path.split(',')


def parse_intersections(output_lines):
    points = set()
    for line in output_lines:
        try:
            x1_bin, y1_bin = line.strip().split(';')
            p_x = bin2float(x1_bin)
            p_y = bin2float(y1_bin)
            points.add((p_x, p_y))
        except ValueError:
            continue
    return sorted(points, key=lambda p: (p[0], p[1]))


def calculate_distances(original_points, approximated_points):
    distances = []
    for (x1, y1), (x2, y2) in zip(original_points, approximated_points):
        dx = x2 - x1
        dy = y2 - y1

        distance = math.sqrt(dx ** 2 + dy ** 2)
        distances.append(distance)
    return distances


def load_points_from_file(filename):
    points = []
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            # Split by semicolon and convert to float
            try:
                x_bin, y_bin = line.strip().split(';')  # Expect binary format
                x = bin2float(x_bin)
                y = bin2float(y_bin)
                points.append((x, y))
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
    return points


# Define default commands
default_commands = [
    #'./testers/test_bo',
    #'./testers/test_boost',
    #'./testers/test_cgal_intersector',
    #'./testers/test_cgal_arrangement',
    #'./testers/test_geo',
    #'./testers/test_ogdf',
    #'./test_geopanda_d.py',
    #'./test_sweeper_ud.py',
    #'./test_decimal5_r.py',
    #'./test_decimal5_ur.py',
    #'./test_decimal25_r.py',
    #'./test_decimal25_ur.py',
    #'./test_decimal50_r.py',
    #'./test_decimal50_ur.py',
    #'./test_decimal75_r.py',
    #'./test_decimal75_ur.py',
    #'./test_decimal100_r.py',
    #'./test_decimal100_ur.py',
    #'./test_double_d.py',
    #'./test_double_ud.py',
    #'./test_toFraction_r.py',
    #'./test_toFraction_ur.py',
    #'./metriX_test.py',
]


def process_file(file, accuracies, commands):
    result_row = [file]
    time_row = [file]
    memory_row = [file]
    distance_row = [file]

    file_basename = os.path.basename(file)
    file_basename = file_basename.split('_', 1)[1]
    accuracy_file_path_d = os.path.join(accuracies, "d_" + file_basename)
    accuracy_file_path_r = os.path.join(accuracies, "r_" + file_basename)
    file_in_accuracies = os.path.exists(accuracy_file_path_d)

    for command in commands:
        # Run the command with the file argument
        command_with_file = f"{command} -f {file}"
        output_lines = run_command(command_with_file)

        if len(output_lines) == 3:
            result, time_taken, memory_usage = output_lines

            # Append to corresponding rows for each table
            result_row.append(result)
            time_row.append(time_taken)  # Splitting to remove "ms" or other suffixes
            memory_row.append(memory_usage)  # Same for memory, take just the number
        else:
            # If the output is not in the expected format, add placeholders
            # print(f"Warning: Output format for {command} with file {file} is unexpected.")
            result_row.append("Error")
            time_row.append("Error")
            memory_row.append("Error")

        if file_in_accuracies:
            file_points_d = load_points_from_file(accuracy_file_path_d)
            file_points_r = load_points_from_file(accuracy_file_path_r)

            command_with_file_a = f"{command} -f {file} -a"
            output_lines_a = run_command(command_with_file_a)

            if output_lines_a and output_lines_a[0] == "p_x;p_y":
                output_lines_a = output_lines_a[1:]

                points = parse_intersections(output_lines_a)

                if re.search(r'_(.*?)d.*?\.', command):
                    if len(file_points_d) != len(points):
                        distance_row.append("Error")
                    else:
                        distances = calculate_distances(file_points_d, points)
                        total_distance = sum(distances)

                        distance_row.append(total_distance)
                elif re.search(r'_(.*?)r.*?\.', command):
                    if len(file_points_r) != len(points):
                        distance_row.append("Error")
                    else:
                        distances = calculate_distances(file_points_r, points)
                        total_distance = sum(distances)

                        distance_row.append(total_distance)
            else:
                distance_row.append("Error")

    return result_row, time_row, memory_row, distance_row


def main():
    parser = argparse.ArgumentParser(description="Run commands with file input.")
    parser.add_argument('-f', '--file', required=True, help='Path to the file, list of files, or folder')
    parser.add_argument('-c', '--commands', help='Comma-separated list of commands to execute')
    parser.add_argument('-a', '--accuracies', required=True, help='Path to the accuracies folder for extra processing')

    args = parser.parse_args()

    # List of shell commands to execute (replace with your actual commands)
    commands = args.commands.split(',') if args.commands else default_commands

    # Get the list of files to process
    files = get_files_from_argument(args.file)

    # Headers for the tables (command names as columns)
    command_headers = ["File"]
    for command in commands:
        # Remove the './testers/test_' prefix and '.py' suffix if present
        header = command.replace('./testers/test_', '').replace('./', '').replace('test_', '').replace('.py', '')
        command_headers.append(header.capitalize())

    # Initialize tables
    result_table = []
    time_table = []
    memory_table = []
    distance_table = []

    total_files = len(files)
    processed_files = 0

    # Use ThreadPoolExecutor to parallelize the processing of files
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        # Submit tasks to the executor for each file
        future_to_file = {executor.submit(process_file, file, args.accuracies, commands): file for file in files}

        for future in concurrent.futures.as_completed(future_to_file):
            try:
                result_row, time_row, memory_row, distance_row = future.result()
                # Append the rows to the tables
                result_table.append(result_row)
                time_table.append(time_row)
                memory_table.append(memory_row)
                if len(distance_row) > 1:
                    distance_table.append(distance_row)
            except Exception as e:
                print(f"File {future_to_file[future]} generated an exception: {e}")

            processed_files += 1
            if processed_files % 10 == 0:  # Print update every 10 files processed
                print(f"Processed {processed_files}/{total_files} files...")


    result_file = "results.csv"
    time_file = "time_taken.csv"
    memory_file = "memory_usage.csv"
    distance_file = "distances.csv"

    with open(result_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(command_headers)  # Write the headers
        writer.writerows(result_table)

    with open(time_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(command_headers)  # Write the headers
        writer.writerows(time_table)

    with open(memory_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(command_headers)  # Write the headers
        writer.writerows(memory_table)

    with open(distance_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(command_headers)  # Write the headers
        writer.writerows(distance_table)

    """
    print("\nResults:")
    print(tabulate(result_table, headers=command_headers, tablefmt="grid"))

    print("\nTime Taken (in ms):")
    print(tabulate(time_table, headers=command_headers, tablefmt="grid"))

    print("\nMemory Usage:")
    print(tabulate(memory_table, headers=command_headers, tablefmt="grid"))

    print("\nTotal Euclidean Distances Between Points:")
    print(tabulate(distance_table, headers=command_headers, tablefmt="grid"))
    """


if __name__ == "__main__":
    main()

