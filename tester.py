import csv
import datetime
import functools
import getpass
import json
import resource
import socket
import sys
import time
import traceback
from collections import defaultdict
from itertools import product

import click
import sh
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from segintbench.utils import *

hostname = socket.gethostname()
username = getpass.getuser()


def parse_timeout(val):
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            t = time.fromisoformat(val)
            return ((t.hour * 60) + t.minute) * 60 + t.second
    else:
        return val


@click.group()
def cli():
    pass


@cli.command()
@click.argument("files", required=True, nargs=-1,
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option("--command", "-c", "commands", multiple=True)
@click.option("--print-intersections", "-a", is_flag=True)
@click.option("--force", "-f", is_flag=True)
@click.option("--retry-failed", "-r", is_flag=True)
@click.option("--timeout", default=None, type=parse_timeout)
@click.option("--outdir", "-o", default=None, type=click.Path(file_okay=False, resolve_path=True))
@click.option("--outstem", default=None)
@click.option("--parallelism", "-p", default=os.cpu_count() - 1)
@click.option("--print-adapters", is_flag=True)
@click.option("--adapters-dir", default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--memory-limit", type=int, default=None,
              help="Maximum memory per test process (in MB)")
def run_tests(commands, files, parallelism, print_adapters, adapters_dir, **kwargs):
    """Locally run one or more adapter on a given set of files"""
    if not kwargs.get("outstem", ""):
        kwargs["outstem"] = Path(os.path.commonpath(Path(f).parent for f in files)).resolve()
    if not kwargs.get("outdir", ""):
        if not kwargs.get("print_intersections", True):
            kwargs["outdir"] = "./out-intersections"
        else:
            kwargs["outdir"] = "./out"

    if not commands or print_adapters:
        adapters_dir = Path(adapters_dir or (Path(__file__).parent / "adapters").resolve())
        if not adapters_dir.is_dir() or not (adapters_dir / "cpp/CMakeLists.txt").is_file():
            raise click.UsageError(f"No command specified and no adapters found in {adapters_dir.resolve()}")
        cpp_adapters = [str(e) for e in (adapters_dir / "cpp/build-release").glob("test_*")]
        if not cpp_adapters:
            print(f"Warning: no built C++ adapters found in {adapters_dir}/cpp/build-release!", file=sys.stderr)
        commands = (
                [str(adapters_dir / "rust/target/release/test_geo"),
                 f"java -jar {adapters_dir / 'java/target/topog-1.0-SNAPSHOT.jar'}"] +
                [f"python3 {e}" for e in (adapters_dir / "python").glob("test_*.py")] + cpp_adapters
        )
        if print_adapters:
            print("\n".join(commands))
            return

    thread_map(functools.partial(test_one, **kwargs),
               product(commands, files), total=len(commands) * len(files), max_workers=parallelism or None)


def test_one(args, *, print_intersections, force, retry_failed, timeout, outdir, outstem, memory_limit):
    command, file = args
    command_file = Path(command.split(" ")[-1])  # simple heuristic that works for all commands above
    outpath = Path(outdir) / command_file.name / Path(file).relative_to(outstem).with_suffix(".out.csv")
    errpath = outpath.with_suffix(".err.txt")
    timepath = outpath.with_suffix(".time.txt")
    metapath = outpath.with_suffix(".meta.json")
    if not force and outpath.exists() and metapath.exists() and (not retry_failed or not errpath.exists()):
        tqdm.write(f"Skipping {file} as output {outpath} already exists")
        return
    outpath.parent.mkdir(parents=True, exist_ok=True)
    for p in (outpath, errpath, timepath, metapath):
        if p.exists():
            p.unlink()

    comm = sh
    comm = comm.time.bake(verbose=True, output=timepath, _cwd=outpath.parent).bake("--")
    if memory_limit:
        max_bytes = memory_limit * 1024 * 1024
        comm.bake(_preexec_fn=lambda: resource.setrlimit(resource.RLIMIT_AS, (max_bytes, max_bytes)))
    if timeout:
        comm = comm.timeout.bake(kill_after=10).bake(timeout)
    comm = comm.bake(*command.split(" "), _err=errpath, _out=outpath)  # _env={}
    if print_intersections:
        comm = comm.bake("-a")

    meta = {
        "starttime": datetime.datetime.now().isoformat(),
        "host": hostname,
        "user": username,
        "input": file,
        "command": command,
        "time": str(timepath),
        "output": str(outpath),
        "error": str(errpath),
        "input_stat": tuple(Path(file).stat()),
        "command_stat": tuple(command_file.stat()),
        "input_md5": sh.md5sum(file),
        "command_md5": sh.md5sum(command_file),
        "print_intersections": print_intersections,
        "force": force,
        "retry_failed": retry_failed,
        "timeout": timeout,
    }

    try:
        comm("-f", file)
        exit_code = 0
    except sh.ErrorReturnCode as e:
        exit_code = e.exit_code
        tqdm.write(f"Command {command_file} failed on {file} with code {exit_code}, check {errpath} for details")

    meta["exit_code"] = exit_code
    meta["endtime"] = datetime.datetime.now().isoformat()
    meta["output_stat"] = tuple(outpath.stat())
    meta["output_md5"] = sh.md5sum(outpath)
    with open(metapath, "w") as f:
        json.dump(meta, f, indent=4)

    if errpath.is_file() and errpath.stat().st_size == 0:
        errpath.unlink()


@cli.command()
@click.argument("dir", required=True, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.argument("out", required=True, type=click.File(mode="w"))
def collect(dir, out):
    dir = Path(dir)
    w = None
    errors = 0
    for metafile in tqdm(dir.rglob("*.meta.json")):
        with open(metafile) as f:
            meta = json.load(f)
        if meta.get("exit_code", None) != 0:
            tqdm.write(f"Failed run in {metafile}: {meta}", file=sys.stderr)
            errors += 1
        for k in ["result", "time", "memory", "uniqfile", "uniqfile_stat", "uniqfile_md5"]:
            meta[k] = None
        try:
            if meta.get("print_intersections", True):
                segs = set(read_segments_from_csv(meta["output"]))
                meta["result"] = len(segs)
                if segs:
                    uniqfile = Path(meta["output"]).with_suffix(".uniq.csv")
                    write_segments_to_csv(sorted(segs), uniqfile, binary_encode=False)
                    meta["uniqfile"] = str(uniqfile)
                    meta["uniqfile_stat"] = tuple(uniqfile.stat())
                    meta["uniqfile_md5"] = sh.md5sum(uniqfile)
            else:
                with open(meta["output"]) as f:
                    meta["result"], meta["time"], meta["memory"] = map(int, f.readlines())
        except Exception as e:
            msg = '\n\t'.join(traceback.format_exception_only(e)).strip()
            tqdm.write(f"Error reading output for {metafile}: {msg}", file=sys.stderr)
            errors += 1

        if not w:
            w = csv.DictWriter(out, meta.keys())
            w.writeheader()
        w.writerow(meta)

    if errors != 0:
        raise click.ClickException(f"{errors} errors encountered while collecting results, see stderr for details")


@cli.command()
@click.argument("csv", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.argument("out", required=True, type=click.File(mode="w"))
@click.option("--tablefmt", "-f", default="github")
@click.option("--key", "-k", default="result")
@click.option("--missing", "-m", default="")
def summarize(csv, out, tablefmt, key, missing):
    summary = defaultdict(dict)
    with open(csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            summary[row["input"]][row["command"]] = str(row[key])

    sorted_inputs = sorted(summary.keys())
    full_commands = set(v.keys() for v in summary.values())
    sorted_full_commands = sorted(full_commands)

    table = []
    for inp in sorted_inputs:
        row = [inp]
        for cmd in sorted_full_commands:
            cell = summary[inp].get(cmd, missing)
            row.append(cell)
        table.append(row)

    headers = ["Input"] + sorted_full_commands

    from tabulate import tabulate
    out.write(tabulate(table, headers=headers, tablefmt=tablefmt))


if __name__ == '__main__':
    cli()
