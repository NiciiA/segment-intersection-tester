import argparse
import os
import shutil
import sys

def delete_folder(path):
    if os.path.exists(path):
        print(f"Deleting: {path}")
        shutil.rmtree(path)
    else:
        print(f"Not found: {path}")

def main():
    parser = argparse.ArgumentParser(description="Clean tester result folders.")
    parser.add_argument("-r", "--results", required=True, help="Path to results folder")
    parser.add_argument("-t", "--testers", nargs="*", help="Names of tester subfolders to delete")

    args = parser.parse_args()
    results_dir = os.path.abspath(args.results)

    if not os.path.exists(results_dir):
        print(f"Results folder does not exist: {results_dir}")
        sys.exit(1)

    if args.testers:
        for tester in args.testers:
            tester_path = os.path.join(results_dir, tester)
            delete_folder(tester_path)
    else:
        delete_folder(results_dir)

if __name__ == "__main__":
    main()
