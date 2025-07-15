import csv
import datetime
import functools
import getpass
import json
import os
import socket
import sys
import time
import traceback
import resource
from itertools import product
from pathlib import Path

import click
import sh
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

hostname = socket.gethostname()
username = getpass.getuser()


def limit_memory(max_mem_mb):
    """Limit max virtual memory for the current process and its children."""
    max_bytes = max_mem_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_bytes, max_bytes))


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


"""
    TODO: add space_limit?
    leda-mm sort of has endless loop
"""


@cli.command()
@click.argument("files", required=True, nargs=-1,
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option("--command", "-c", "commands", multiple=True)
@click.option("--print-intersections", "-a", is_flag=True)
@click.option("--force", is_flag=True)
@click.option("--retry-failed", "-r", is_flag=True)
@click.option("--timeout", default=None, type=parse_timeout)
@click.option("--outdir", "-o", default="./out", type=click.Path(file_okay=False, resolve_path=True))
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

    thread_map(functools.partial(test_one, memory_limit=kwargs.get("memory_limit"), **kwargs),
               product(commands, files), total=len(commands) * len(files), max_workers=parallelism or None)


def test_one(args, *, print_intersections, force, retry_failed, timeout, outdir, outstem, memory_limit=None):
    if memory_limit:
        try:
            limit_memory(memory_limit)
        except Exception as e:
            tqdm.write(f"could not set memory limit: {e}")

    command, file = args
    command_file = Path(command.split(" ")[-1])
    outpath = Path(outdir)
    if print_intersections:
        outpath = outpath / "print_intersections"
    outpath = outpath / command_file.name / Path(file).relative_to(outstem).with_suffix(".out.csv")
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
    for metafile in tqdm(dir.rglob("*.meta.json")):
        with open(metafile) as f:
            meta = json.load(f)
        try:
            with open(meta["output"]) as f:
                meta["result"], meta["time"], meta["memory"] = map(int, f.readlines())
        except Exception as e:
            meta["result"] = meta["time"] = meta["memory"] = None
            msg = '\n\t'.join(traceback.format_exception_only(e)).strip()
            tqdm.write(f"Error reading output for {metafile}: {msg}",
                       file=sys.stderr)
        if not w:
            w = csv.DictWriter(out, meta.keys())
            w.writeheader()
        w.writerow(meta)


"""
    TODO: sanity check, rückgabe wert 0 und resultat dann gut,
                        rückgabe wert != 0 und resultat dann console log
                        rückgabe wert 0 und kein resultat dann console log
                        rückgabe wert != und kein resultet dann error.txt mit graceful und ungraceful
"""


if __name__ == '__main__':
    cli()
