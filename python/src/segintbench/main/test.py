import concurrent
import csv
import datetime
import functools
import getpass
import json
import resource
import socket
import sys
import traceback
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from itertools import product

import sh
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from segintbench.fast_inter import calculate_intersections_vectorized, IntersectionType
from segintbench.utils import *

hostname = socket.gethostname()
username = getpass.getuser()


@click.group()
def cli():
    pass


def get_adapters(adapters_dir):
    adapters_dir = Path(adapters_dir or f"{__file__}/../../../../../adapters").resolve()
    if not adapters_dir.is_dir() or not (adapters_dir / "cpp/CMakeLists.txt").is_file():
        raise click.UsageError(f"No command specified and no adapters found in {adapters_dir.resolve()}")
    cpp_adapters = [str(e) for e in (adapters_dir / "cpp/build-release").glob("test_*")]
    if not cpp_adapters:
        print(f"Warning: no built C++ adapters found in {adapters_dir}/cpp/build-release!", file=sys.stderr)
    return (
            [str(adapters_dir / "rust/target/release/test_geo"),
             f"java -jar {adapters_dir / 'java/target/topog-1.0-SNAPSHOT.jar'}"] +
            [f"python3 {e}" for e in (adapters_dir / "python").glob("test_*.py")] + cpp_adapters
    )


@cli.command()
@click.option("--adapters-dir", default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True))
def print_adapters(adapters_dir):
    print("\n".join(get_adapters(adapters_dir)))


@cli.command()
@click.argument("files", required=True, nargs=-1)
@click.option("--command", "-c", "commands", multiple=True)
@click.option("--print-intersections", "-a", is_flag=True)
@click.option("--force", "-f", is_flag=True)
@click.option("--retry-failed", "-r", is_flag=True)
@click.option("--timeout", default=None, type=parse_timeout)
@click.option("--outdir", "-o", default=None, type=click.Path(file_okay=False, resolve_path=True))
@click.option("--outstem", default=None)
@click.option("--parallelism", "-p", default=os.cpu_count() - 1)
@click.option("--adapters-dir", default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--memory-limit", type=int, default=None,
              help="Maximum memory per test process (in MB)")
def run(commands, files, parallelism, adapters_dir, **kwargs):
    """Locally run one or more adapter on a given set of files"""
    files = [f.absolute() for f in parse_files(files, "*.csv")]
    if not kwargs.get("outstem", ""):
        kwargs["outstem"] = Path(os.path.commonpath(Path(f).parent for f in files)).resolve()
    if not kwargs.get("outdir", ""):
        if kwargs.get("print_intersections", False):
            kwargs["outdir"] = Path("./out-intersections")
        else:
            kwargs["outdir"] = Path("./out")

    if not commands:
        commands = get_adapters(adapters_dir)

    thread_map(functools.partial(test_one, **kwargs),
               product(commands, files), total=len(commands) * len(files), max_workers=parallelism or None)


def test_one(args, *, print_intersections, force, retry_failed, timeout, outdir, outstem, memory_limit):
    command, file = args
    command_file = Path(command.split(" ")[-1])  # simple heuristic that works for all commands above
    basepath = Path(outdir).absolute() / command_file.name / Path(file).relative_to(outstem)
    outpath = basepath.with_suffix(".out.csv")
    errpath = basepath.with_suffix(".err.txt")
    timepath = basepath.with_suffix(".time.txt")
    metapath = basepath.with_suffix(".meta.json")
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
        "input": str(file),
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
@click.argument("files", required=True, nargs=-1)
@click.argument("out", required=True, type=click.File(mode="w"))
@click.option("--timeout", default=None, type=parse_timeout)
@click.option("--parallelism", "-p", default=os.cpu_count() - 1)
def stat(files, out, timeout, parallelism):
    files = list(parse_files(files, "*.csv"))
    w = None
    with tqdm(total=len(files)) as pb:
        with ProcessPoolExecutor(max_workers=parallelism or None) as ex:
            fs = [ex.submit(stat_one_file, f) for f in files]
            while fs:
                res = concurrent.futures.wait(fs, timeout=timeout, return_when=concurrent.futures.FIRST_COMPLETED)
                if not res.done:
                    for future in fs:
                        future.cancel()
                    raise click.ClickException(f"Timeout reached! {len(res.not_done)} pending tasks: {res.not_done}")
                else:
                    for future in res.done:
                        try:
                            row = future.result(0)  # This will raise an exception if the task failed
                            if not w:
                                w = csv.DictWriter(out, row.keys())
                                w.writeheader()
                            w.writerow(row)
                        except Exception as e:
                            print(f"An error occurred: {e}")
                        pb.update(len(res.done))
                    fs = res.not_done


def stat_one_file(file):
    tqdm.write(f"start: {file}")
    segs = list(read_segments_from_csv(file, decode=lambda x: Fraction(bin2float(x))))
    n = len(segs)

    length_0 = horiz = vert = 0
    points = set()
    for seg in segs:
        if seg[0] == seg[1]:
            length_0 += 1
        elif seg[0][0] == seg[1][0]:
            horiz += 1
        elif seg[0][1] == seg[1][1]:
            vert += 1
        points.update(seg)

    same_x = length_0 or vert
    same_y = length_0 or horiz
    if not same_x:
        same_x = len(set(*(s.p1.x, s.p2.x) for s in segs)) != len(segs) * 2
    if not same_y:
        same_y = len(set(*(s.p1.y, s.p2.y) for s in segs)) != len(segs) * 2

    overlap = online = intersect = 0
    inter_points = set()
    for e in calculate_intersections_vectorized(segs):
        if e[0] == IntersectionType.SEGMENT_OVERLAP:
            overlap += 1
        elif e[0] == IntersectionType.POINT_OVERLAP:
            online += 1
        elif e[0] == IntersectionType.TRUE_INTERSECTION:
            intersect += 1
            inter_points.add(e[3])

    tqdm.write(f"done: {file}")
    return {
        "file": file, "segs": n, "combs": n * (n - 1) // 2,
        "points": len(points), "intersection_points": len(inter_points),
        "true_intersection_points": len(inter_points - points),
        "length_0": length_0, "horiz": horiz, "vert": vert, "same_x": same_x, "same_y": same_y,
        "overlap": overlap, "online": online, "intersect": intersect,
    }


@cli.command()
@click.argument("files", required=True, nargs=-1)
@click.argument("out", required=True, type=click.File(mode="w"))
def collect(files, out):
    files = list(parse_files(files, "*.meta.json"))
    w = None
    errors = 0
    for metafile in tqdm(files):
        with open(metafile) as f:
            meta = json.load(f)
        for k in ["result", "time", "memory", "uniqfile", "uniqfile_stat", "uniqfile_md5"]:
            meta[k] = None
        if meta.get("exit_code", None) != 0:
            tqdm.write(f"Failed run in {metafile} with exit code {meta.get('exit_code', None)}", file=sys.stderr)
            errors += 1
        else:
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
@click.argument("file", required=True, type=click.File('rt'))
@click.argument("out", required=True, type=click.File('wt'))
@click.option("--tablefmt", "-f", default="github")
@click.option("--key", "-k", default="result")
@click.option("--missing", "-m", default="")
def summarize(file, out, tablefmt, key, missing):
    summary = defaultdict(dict)
    for row in csv.DictReader(file):
        summary[row["input"]][row["command"]] = str(row[key])

    sorted_inputs = sorted(summary.keys())
    full_commands = set(itertools.chain.from_iterable(v.keys() for v in summary.values()))
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
