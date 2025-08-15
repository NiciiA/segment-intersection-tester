import json
import random

import click

from segintbench.utils import *


@click.group()
def cli():
    pass


@cli.command()
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
@click.option('--binary/--string', '-b/-s', is_flag=True, default=True)
def from_json(input, output, binary):
    data = json.load(input)
    nodes = {n["id"]: Point(n["x"], n["y"]) for n in data["nodes"]}
    write_segments_to_csv((
        Segment(nodes[e["source"]], nodes[e["target"]])
        for e in data["edges"]
    ), output, binary_encode=binary)


@cli.command()
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
@click.option('--min', type=float, default=0.9)
@click.option('--max', type=float, default=1.1)
@click.option('--seed', default=None)
def randomize_lengths(input, output, min, max, seed):
    random.seed(seed)
    write_segments_to_csv((
        s.scale(random.uniform(min, max))
        for s in read_segments_from_csv(input)
    ), output)


@cli.command()
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
@click.option('--seed', default=None)
def randomize_lengths(input, output, seed):
    random.seed(seed)
    segs = list(read_segments_from_csv(input))
    random.shuffle(segs)
    write_segments_to_csv(segs, output)


@cli.command()
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
def float2bin(input, output):
    write_segments_to_csv(list(read_segments_from_csv(input, float)), output, binary_encode=True)


@cli.command()
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
def bin2float(input, output):
    write_segments_to_csv(list(read_segments_from_csv(input)), output, binary_encode=False)


if __name__ == '__main__':
    cli()
