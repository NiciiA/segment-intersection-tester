import argparse
import shutil
import subprocess


def test_file(tester_path, filepath):
    """
    Test if the file triggers an error using the specified tester executable.
    Returns True if the error occurs, False otherwise.
    """
    try:
        result = subprocess.run(
            [tester_path, "-f", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode != 0  # Return True if the command fails
    except FileNotFoundError:
        print(f"Error: Tester executable '{tester_path}' not found or not executable.")
        exit(1)


def write_file(filepath, header, lines):
    """
    Write a new file with the given lines.
    """
    with open(filepath, "w") as f:
        f.write(header)
        f.writelines(lines)


def minimize_file(tester_path, input_file, output_file):
    """
    Iteratively remove lines and test the file to minimize the error-causing instance.
    """
    with open(input_file, "r") as f:
        lines = f.readlines()

    header = lines[0]  # Extract the header
    data = lines[1:]  # Extract the data lines

    # Initial check if the entire file causes an error
    if not test_file(tester_path, input_file):
        print("The input file does not cause an error. Exiting.")
        return

    print(f"Original file causes an error with {len(data)} lines.")

    removed = 1
    while removed:
        removed = 0
        i = 0
        while i < len(data):
            # Create a copy without the current line
            reduced_data = data[:i] + data[i + 1:]
            write_file(output_file, header, reduced_data)

            if test_file(tester_path, output_file):
                # If the reduced file still causes an error, update the data
                print(f"Error persists after removing line {i + 1 + removed}.")
                data = reduced_data
                removed += 1
            else:
                # Otherwise, keep the line and move to the next
                print(f"Error resolved after removing line {i + 1 + removed}. Keeping it.")
                i += 1

    # Write the final minimized file
    write_file(output_file, header, data)
    print(f"Minimized file written with {len(data)} lines.")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Minimize a CSV file to the smallest instance that triggers an error.")
    parser.add_argument("-t", "--tester", required=True, help="Path to the tester executable.")
    parser.add_argument("-i", "--input_file", required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_file", required=True, help="Path to save the minimized CSV file.")

    args = parser.parse_args()

    # Check if tester executable exists
    if not shutil.which(args.tester):
        print(f"Error: Tester executable '{args.tester}' not found.")
        exit(1)

    # Minimize the file
    minimize_file(args.tester, args.input_file, args.output_file)


if __name__ == "__main__":
    main()
