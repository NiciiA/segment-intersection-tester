import functools
import pprint
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


def build_cmd(prefix, filepath, suffix):
    first_cmd = f"{prefix} {suffix}"
    if "%1" in first_cmd:
        first_cmd = first_cmd % filepath
    else:
        first_cmd = f"{prefix} -f {filepath} {suffix}"
    first_cmd = first_cmd.strip()
    return first_cmd


def test_differs(first, second, suffix, allow_fail, verbose, filepath):
    filepath = shlex.quote(filepath)
    cmds = {pre: build_cmd(pre, filepath, suffix) for pre in first + second}
    # if verbose >= 2:
    #     print("Running")
    #     pprint.pprint({c: cmds[c] for c in first}, width=200)
    #     pprint.pprint({c: cmds[c] for c in second}, width=200)
    res = {pre: subprocess.run(cmd, capture_output=True, shell=True) for pre, cmd in cmds.items()}
    if not allow_fail and any(r.returncode != 0 or r.stderr for r in res.values()):
        print("Some commands failed:", file=sys.stderr)
        pprint.pprint(res, stream=sys.stderr, width=200)
        exit(1)
    elif verbose >= 2:
        print("Results:")
        pprint.pprint(res, width=200)
    resv = {
        pre: run.returncode or run.stdout.decode().strip().splitlines()
        for pre, run in res.items()
    }
    ref = resv[first[0]]
    still_differs = True
    for pre in first:
        if resv[pre] != ref:
            still_differs = False
            if verbose >= 3:
                print(f"Result for {pre} differs from {first[0]} but shouldn't!")
                # print("== <DIFF> ==")
                # print('\n'.join(difflib.ndiff(ref, resv[pre])))
                # print("== </DIFF> ==")
    for pre in second:
        if resv[pre] == ref:
            still_differs = False
            if verbose >= 3:
                print(f"Result for {pre} matches {first[0]} but shouldn't!")
    return still_differs


@click.command()
@click.argument('input', type=click.Path(dir_okay=False, exists=True, readable=True))
@click.argument('output', type=click.Path(dir_okay=False, writable=True))
@click.option('--first', '-a', default=[], multiple=True)
@click.option('--second', '-b', default=[], multiple=True)
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
