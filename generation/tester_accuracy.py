import math
import os
import re
import struct


# TODO update main tester.py to check accuracy?

def bin2float(binary_string, single=False):
    if len(binary_string) != (32 if single else 64):
        raise ValueError("Binary string length must be 32 (for float) or 64 (for double).")
    byte_data = int(binary_string, 2).to_bytes(4 if single else 8, byteorder='big')
    return struct.unpack('>f' if single else '>d', byte_data)[0]


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
