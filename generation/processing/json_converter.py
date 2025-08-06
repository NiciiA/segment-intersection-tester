import json

import click


@click.command()
@click.argument('file', type=click.File('rt'))
def parse(file):
    data = json.load(file)
    nodes = {n["id"]: (n["x"], n["y"]) for n in data["nodes"]}
    for e in data["edges"]:
        print(";".join(map(str, nodes[e["source"]] + nodes[e["target"]])))


if __name__ == '__main__':
    parse()
