import argparse
import subprocess
import os

def run_in_dir(directory, command):
    print(f"\n==> Running in {directory}: {' '.join(command)}")
    full_dir = os.path.abspath(directory)
    subprocess.run(command, cwd=full_dir, check=True)

def do_generation():
    run_in_dir("generation/generator", ["python", "./generation/generator.py"])
    run_in_dir("generation/locations", ["python", "./generation/generate_locations.py"])

def do_testing():
    run_in_dir("testing/tests", ["python", "./tester.py", "run-tests", "./data/segment-intersection-data/tests/*"])
    run_in_dir("testing/loctests", ["python", "./tester.py", "run-tests", "./data/segment-intersection-data/tests_location/*"])
    run_in_dir("testing/collecter", ["python", "./tester.py", "collect", "./out", "results.csv"])

def main():
    parser = argparse.ArgumentParser(description="Run test generation and/or execution pipeline.")
    parser.add_argument("-g", "--generate", action="store_true", help="Run generation steps")
    parser.add_argument("-t", "--test", action="store_true", help="Run testing steps")
    args = parser.parse_args()

    if args.generate:
        do_generation()

    if args.test:
        do_testing()

    if not args.generate and not args.test:
        print("Nothing to do. Use -g to generate or -t to test.")

if __name__ == "__main__":
    main()
