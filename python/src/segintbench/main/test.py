import collections
import concurrent
import csv
import datetime
import functools
import getpass
import json
import pprint
import resource
import socket
import sys
import traceback
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from itertools import product
from json import JSONDecodeError
from textwrap import indent

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


def get_adapters(adapters_dir, exclude=None, only=None):
    adapters_dir = Path(adapters_dir or f"{__file__}/../../../../../adapters").resolve()
    if not adapters_dir.is_dir() or not (adapters_dir / "cpp/CMakeLists.txt").is_file():
        raise click.UsageError(f"No command specified and no adapters found in {adapters_dir.resolve()}")

    cpp_adapters = [str(e) for e in (adapters_dir / "cpp/build-release").glob("test_*")]
    if not cpp_adapters:
        print(f"Warning: no built C++ adapters found in {adapters_dir}/cpp/build-release!", file=sys.stderr)

    adapters = [str(adapters_dir / "rust/target/release/test_geo"),
                f"java -jar {adapters_dir / 'java/target/topog-1.0-SNAPSHOT.jar'}"]
    adapters.extend(f"python3 {e}" for e in (adapters_dir / "python").glob("test_*.py"))
    adapters.extend(cpp_adapters)

    if exclude:
        adapters = [a for a in adapters if not re.search(exclude, a)]
    if only:
        adapters = [a for a in adapters if re.search(only, a)]

    return adapters


@cli.command()
@click.option("--adapters-dir", default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--exclude-commands", "-n", default=None)
@click.option("--only-commands", "-j", default=None)
def print_adapters(adapters_dir, exclude_commands, only_commands):
    print("\n".join(get_adapters(adapters_dir, exclude_commands, only_commands)))


@cli.command()
@click.argument("files", required=True, nargs=-1)
@click.option("--exclude-files", "-e", default=None)
@click.option("--print-intersections", "-a", is_flag=True)
@click.option("--outdir", "-o", default=None, type=click.Path(file_okay=False, resolve_path=True))
@click.option("--outstem", "-s", default=None)
@click.option("--command", "-c", "commands", multiple=True)
@click.option("--adapters-dir", default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--exclude-commands", "-n", default=None)
@click.option("--only-commands", "-j", default=None)
@click.option("--parallelism", "-p", default=os.cpu_count() - 1)
@click.option("--force", "-f", is_flag=True)
@click.option("--quiet/--verbose", "-q/-v", is_flag=True, default=True)
@click.option("--retry-failed", "-r", is_flag=True)
@click.option("--timeout", "-t", default=None, type=parse_timeout)
@click.option("--memory-limit", "-m", type=int, default=None,
              help="Maximum memory per test process (in MB)")
def run(commands, files, parallelism, adapters_dir, exclude_files, exclude_commands, only_commands, **kwargs):
    """Locally run one or more adapter on a given set of files"""
    files = [f.absolute() for f in parse_files(files, "*.csv", exclude_files)]
    if not kwargs.get("outstem", ""):
        kwargs["outstem"] = Path(os.path.commonpath(Path(f).parent for f in files)).resolve()
    if not kwargs.get("outdir", ""):
        if kwargs.get("print_intersections", False):
            kwargs["outdir"] = Path("./out-intersections")
        else:
            kwargs["outdir"] = Path("./out")

    if not commands:
        commands = get_adapters(adapters_dir, exclude_commands, only_commands)

    thread_map(functools.partial(test_one, **kwargs),
               product(commands, files), total=len(commands) * len(files), max_workers=parallelism or None)


def test_one(args, *, print_intersections, force, retry_failed, timeout, outdir, outstem, memory_limit, quiet):
    command, file = args
    command_file = get_command_file(command)
    basepath = Path(outdir).absolute() / command_file.name / Path(file).relative_to(outstem)
    outpath = basepath.with_suffix(".out.csv")
    uniqpath = basepath.with_suffix(".uniq.csv")
    errpath = basepath.with_suffix(".err.txt")
    timepath = basepath.with_suffix(".time.txt")
    metapath = basepath.with_suffix(".meta.json")
    if not force and outpath.exists() and metapath.exists() and (not retry_failed or not errpath.exists()):
        if not quiet:
            tqdm.write(f"Skipping {file} as output {outpath} already exists")
        return
    outpath.parent.mkdir(parents=True, exist_ok=True)
    for p in (outpath, errpath, timepath, metapath, uniqpath):
        if p.exists():
            p.unlink()

    comm = sh
    comm = comm.time.bake(verbose=True, output=timepath, _cwd=outpath.parent).bake("--")
    if memory_limit:
        max_bytes = memory_limit * 1024 * 1024
        comm = comm.bake(_preexec_fn=lambda: resource.setrlimit(resource.RLIMIT_AS, (max_bytes, max_bytes)))
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
        "input_md5": sh.md5sum(file).strip(),
        "command_md5": sh.md5sum(command_file).strip(),
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
        if not quiet:
            tqdm.write(f"Command {command_file} failed on {file} with code {exit_code}, check {errpath} for details")

    meta["exit_code"] = exit_code
    meta["endtime"] = datetime.datetime.now().isoformat()
    meta["output_stat"] = tuple(outpath.stat())
    meta["output_md5"] = sh.md5sum(outpath).strip()
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
    # tqdm.write(f"start: {file}")
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

    # same_x = length_0 or vert
    # same_y = length_0 or horiz
    # if not same_x:
    same_x = (len(segs) * 2) - len(set(itertools.chain.from_iterable((s.p1.x, s.p2.x) for s in segs)))
    # if not same_y:
    same_y = (len(segs) * 2) - len(set(itertools.chain.from_iterable((s.p1.y, s.p2.y) for s in segs)))

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

    # tqdm.write(f"done: {file}")
    return {
        "file": file, "segs": n, "combs": n * (n - 1) // 2,
        "points": len(points), "intersection_points": len(inter_points),
        "true_intersection_points": len(inter_points - points),
        "length_0": length_0, "horiz": horiz, "vert": vert, "same_x": same_x, "same_y": same_y,
        "same_p": (len(segs) * 2) - len(points),
        "overlap": overlap, "online": online, "intersect": intersect,
    }


@cli.command()
@click.argument("files", required=True, nargs=-1)
@click.argument("out", required=True, type=click.File(mode="w"))
def collect(files, out):
    files = list(parse_files(files, "*.meta.json"))
    w = None
    errors = failed_runs = 0
    failed_cmds = collections.Counter()
    failed_files = collections.Counter()
    for metafile in tqdm(files):
        with open(metafile) as f:
            try:
                meta = json.load(f)
            except JSONDecodeError as e:
                tqdm.write(f"Corrupt meta data {metafile}: {e}", file=sys.stderr)
                errors += 1
                continue
        for k in ["result", "result_uniq", "time", "memory", "uniqfile", "uniqfile_stat", "uniqfile_md5"]:
            meta[k] = None
        if meta.get("exit_code", None) != 0:
            tqdm.write(f"Failed run in {metafile} with exit code {meta.get('exit_code', None)}", file=sys.stderr)
            failed_runs += 1
            failed_cmds[meta["command"]] += 1
            failed_files[meta["input"]] += 1
        else:
            try:
                if meta.get("print_intersections", True):
                    with open(meta["output"], "rt") as csvfile:
                        header = next(csvfile).strip()
                        if header != 'p_x;p_y':  # Skip the header line
                            raise IOError(f"Invalid CSV header {header!r}.")
                        segs_count = 0
                        segs = set()
                        for row in csvfile.readlines():
                            segs_count += 1
                            segs.add(row)
                        meta["result_uniq"] = segs_count
                        meta["result"] = len(segs)

                    if segs:
                        uniqfile = Path(meta["output"]).with_suffix(".uniq.csv")
                        with open(uniqfile, "wt") as csvfile:
                            csvfile.write("p_x;p_y\n")
                            csvfile.writelines(sorted(segs))
                        meta["uniqfile"] = str(uniqfile)
                        meta["uniqfile_stat"] = tuple(uniqfile.stat())
                        meta["uniqfile_md5"] = sh.md5sum(uniqfile).strip()
                else:
                    with open(meta["output"]) as f:
                        meta["result"], meta["time"], meta["memory"] = map(int, f.readlines())

            except Exception as e:
                msg = '\n\t'.join(traceback.format_exception_only(e)).strip()
                tqdm.write(f"Error reading output for {metafile}: {msg}", file=sys.stderr)
                errors += 1
                failed_cmds[meta["command"]] += 1
                failed_files[meta["input"]] += 1

        if not w:
            w = csv.DictWriter(out, meta.keys())
            w.writeheader()
        w.writerow(meta)

    if failed_runs != 0:
        tqdm.write(f"Found {failed_runs} failed runs!", file=sys.stderr)
        tqdm.write(f"Failures/errors per command:\n{pprint.pformat(failed_cmds)}", file=sys.stderr)
        tqdm.write(f"Failures/errors per file:\n{pprint.pformat(failed_files)}", file=sys.stderr)
    if errors != 0:
        raise click.ClickException(f"{errors} errors encountered while collecting results, see stderr for details")
    else:
        tqdm.write(f"Successfully processed {len(files)} files!")


@cli.command()
@click.argument("file", required=True, type=click.File('rt'))
@click.argument("out", required=True, type=click.File('wt'))
@click.option("--tablefmt", "-f", default="github")
@click.option("--key", "-k", default="result")
@click.option("--missing", "-m", default="")
@click.option("--exclude-files", "-e", default=None)
@click.option("--only-files", "-o", default=None)
@click.option("--exclude-commands", "-n", default=None)
@click.option("--only-commands", "-c", default=None)
@click.option("--reference", "-r", default=None)
@click.option("--stat", "-s", default=None, type=click.File('rt'))
@click.option("--stat-base", "-b", default="")
def summarize(file, out, tablefmt, key, missing, exclude_files, only_files, exclude_commands, only_commands, reference,
              stat, stat_base):
    if stat:
        stats = {stat_base + row["file"]: row for row in csv.DictReader(stat)}
    else:
        stats = {}

    summary = defaultdict(dict)
    for row in csv.DictReader(file):
        if exclude_files and re.search(exclude_files, row["input"]):
            continue
        if only_files and not re.search(only_files, row["input"]):
            continue
        summary[row["input"]][row["command"]] = str(row[key])

    sorted_inputs = sorted(summary.keys())
    full_commands = sorted(set(itertools.chain.from_iterable(v.keys() for v in summary.values())))
    print(f"Found {len(full_commands)} commands:", file=sys.stderr)
    print(indent("\n".join(full_commands), "\t"), file=sys.stderr)
    if exclude_commands:
        full_commands = [c for c in full_commands if not re.search(exclude_commands, c)]
    if only_commands:
        full_commands = [c for c in full_commands if re.search(only_commands, c)]
    if exclude_commands or only_commands:
        print(f"Selected {len(full_commands)} commands:", file=sys.stderr)
        print(indent("\n".join(full_commands), "\t"), file=sys.stderr)

    table = []
    for inp in sorted_inputs:
        row = [inp]
        ref = None
        if reference:
            ref = summary[inp].get(reference, None)
        for cmd in full_commands:
            cell = summary[inp].get(cmd, missing)
            if ref is not None and (cell != ref and cell != missing):
                cell = f"**{cell}**"
            row.append(cell)
        if stats and inp in stats:
            s = stats[inp]
            s.pop("file", None)
            row.extend(s.values())
        table.append(row)

    headers = ["Input"] + [get_command_file(c).name for c in full_commands] + list(
        stats[sorted_inputs[0]].keys()) if stats else []

    from tabulate import tabulate
    out.write(tabulate(table, headers=headers, tablefmt=tablefmt))

    print(f"Wrote {len(sorted_inputs)} rows", file=sys.stderr)


if __name__ == '__main__':
    cli()
