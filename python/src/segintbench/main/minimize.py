import difflib
import functools
import shlex
import subprocess
import sys

import click

from segintbench.utils import read_segments_from_csv, write_segments_to_csv


def test_fails(tester_path, verbose, filepath):
    try:
        if "%1" in tester_path:
            args = shlex.split(tester_path % shlex.quote(filepath))
        else:
            args = [tester_path, "-f", filepath]
        if verbose >= 2:
            print(f"Running {' '.join(args)}")
        result = subprocess.run(
            args,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        if verbose:
            print(f"Exit code {result.returncode}")
        return result.returncode != 0  # Return True if the command fails
    except FileNotFoundError:
        print(f"Error: Tester executable '{tester_path}' not found or not executable.", file=sys.stderr)
        exit(1)


def test_differs(first, second, suffix, allow_fail, verbose, filepath):
    filepath = shlex.quote(filepath)
    first_cmd = f"{first} {suffix}"
    if "%1" in first_cmd:
        first_cmd = first_cmd % filepath
    else:
        first_cmd = f"{first} -f {filepath} {suffix}"
    first_cmd = first_cmd.strip()

    second_cmd = f"{second} {suffix}".strip()
    if "%1" in second_cmd:
        second_cmd = second_cmd % filepath
    else:
        second_cmd = f"{second} -f {filepath} {suffix}"
    second_cmd = second_cmd.strip()

    if verbose >= 2:
        print(f"Running\n\t{first_cmd}\n\t{second_cmd}")

    try:
        first_res = subprocess.run(
            first_cmd,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            shell=True
        )
        second_res = subprocess.run(
            second_cmd,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            shell=True
        )

        if allow_fail:
            if first_res.returncode != 0:
                if second_res.returncode != 0:
                    print(f"Both commands failed with codes {first_res.returncode} and {second_res.returncode}")
                    return False
                else:
                    print(f"First command failed with code {first_res.returncode}!")
                    return True
            elif second_res.returncode != 0:
                print(f"Second command failed with code {second_res.returncode}!")
                return True
        else:
            if first_res.returncode != 0:
                if second_res.returncode != 0:
                    print(f"Error: Both commands failed with codes {first_res.returncode} and {second_res.returncode}!",
                          file=sys.stderr)
                    exit(1)
                else:
                    print(f"Error: First command failed with code {first_res.returncode}!", file=sys.stderr)
                    exit(1)
            elif second_res.returncode != 0:
                print(f"Error: Second command failed with code {second_res.returncode}!", file=sys.stderr)
                exit(1)

        out1, out2 = first_res.stdout.decode().strip().splitlines(), second_res.stdout.decode().strip().splitlines()
        if out1 != out2:
            if verbose:
                print("== <DIFF> ==")
                print('\n'.join(difflib.ndiff(out1, out2)))
                print("== </DIFF> ==")
            return True
        else:
            return False
    except FileNotFoundError:
        print("Error: Tester executable not found or not executable.", file=sys.stderr)
        exit(1)


@click.command()
@click.argument('input', type=click.Path(dir_okay=False, exists=True, readable=True))
@click.argument('output', type=click.Path(dir_okay=False, writable=True))
@click.option('--first', '-a', default="")
@click.option('--second', '-b', default="")
@click.option('--suffix', '-c', default="")
@click.option('--test', '-t', default="")
@click.option("--allow-fail", is_flag=True)
@click.option("--verbose", '-v', count=True)
def main(input, output, first, second, suffix, test, allow_fail, verbose):
    if test:
        if first or second or suffix or allow_fail:
            raise click.ClickException("Cannot give (--first, --second, --suffix, --allow-fail) together with --test")
        tester = functools.partial(test_fails, tester_path=test, verbose=verbose)
    else:
        if not first or not second:
            raise click.ClickException("Need to give either --first and --second or --test")
        tester = functools.partial(test_differs, first=first, second=second, suffix=suffix, allow_fail=allow_fail,
                                   verbose=verbose)

    if not tester(filepath=input):
        print("The input file does not cause an error. Exiting.")
        exit(1)

    data = list(read_segments_from_csv(input))
    print(f"Original file causes an error with {len(data)} lines.")

    removed = 1
    while removed:
        removed = 0
        i = 0
        while i < len(data):
            # Create a copy without the current line
            reduced_data = data[:i] + data[i + 1:]
            write_segments_to_csv(reduced_data, output)

            if tester(filepath=output):
                # If the reduced file still causes an error, update the data
                print(f"Error persists after removing line {i + 1 + removed}.")
                data = reduced_data
                removed += 1
            else:
                # Otherwise, keep the line and move to the next
                print(f"Error resolved after removing line {i + 1 + removed}. Keeping it.")
                i += 1

    write_segments_to_csv(data, output)
    print(f"Minimized file written with {len(data)} lines.")

    if verbose:
        print("Final comparison:")
        tester(filepath=output)


if __name__ == "__main__":
    main()
