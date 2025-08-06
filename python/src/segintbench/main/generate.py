import functools
import re
import json

import click
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from segintbench.testcases import CONFIGURATIONS
from segintbench.utils import *


@click.group()
def cli():
    pass


def process_configuration(config, *, output_dir, force):
    func, params, filename, category = config
    filepath = Path(output_dir) / category / filename
    if filepath.is_file() and not force:
        tqdm.write(f"skipped: {filepath}")
    else:
        segments = func(*params)
        write_segments_to_csv(segments, filepath)
        tqdm.write(f"done: {filename}")


@cli.command()
@click.option("--output-dir", "-o", default="tests",
              type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True))
@click.option("--include", default=None)
@click.option("--exclude", default=None)
@click.option("--force", default=False)
@click.option("--parallelism", "-p", default=os.cpu_count() - 1)
def generate_testcases(include, exclude, parallelism, **kwargs):
    incl_re = re.compile(include) if include else None
    excl_re = re.compile(exclude) if exclude else None
    thread_map(functools.partial(process_configuration, **kwargs), [
        c for c in CONFIGURATIONS if
        (not include or incl_re.match(f"{c[3]}/{c[2]}")) and (not exclude or not excl_re.match(f"{c[3]}/{c[2]}"))
    ], max_workers=parallelism or None)


def extract_segments_from_geojson(filepath: str):
    """Yield segments as (x1, y1, x2, y2) from a GeoJSON file."""
    with open(filepath, 'r') as f:
        geojson = json.load(f)

    for feature in geojson.get("features", []):
        coords = feature.get("geometry", {}).get("coordinates", [])
        for i in range(len(coords) - 1):
            yield Segment(Point(coords[i][0], coords[i][1]), Point(coords[i + 1][0], coords[i + 1][1]))


def download_street_network(place: str, network_type: str, output_path):
    """Download and save a street network GeoJSON from a place name."""
    import osmnx as ox
    print(f"Downloading '{network_type}' network for: {place}")
    G = ox.graph_from_place(place, network_type=network_type)
    edges = ox.graph_to_gdfs(G, nodes=False)
    edges.to_file(output_path, driver='GeoJSON')
    print(f"Saved to {output_path}")


@cli.command()
@click.option(
    '-p', '--place',
    type=str,
    default='Innere Stadt, Vienna, Austria',
    help='Place name to query (e.g. "Innere Stadt, Vienna, Austria")')
@click.option(
    '-n', '--network',
    type=click.Choice(['drive', 'walk', 'bike', 'all', 'all_private']),
    default='drive',
    help='Type of network to download (default: drive)')
@click.option(
    '-o', '--output',
    type=click.Path(dir_okay=False, resolve_path=True),
    default='streets.geojson',
    help='Output file name (default: streets.geojson)')
def geo_download(place, network, output):
    download_street_network(place, network, output)


@cli.command()
@click.argument("input", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.argument("output", type=click.Path(dir_okay=False, resolve_path=True))
@click.option("--binary", default=True, is_flag=True)
def geo_convert(input, output, binary):
    segments = extract_segments_from_geojson(input)
    write_segments_to_csv(segments, output, binary_encode=binary)


@cli.command()
@click.option("--output-dir", "-o", default="tests/locations")
@click.option(
    '-n', '--network',
    type=click.Choice(['drive', 'walk', 'bike', 'all', 'all_private']),
    default='drive',
    help='Type of network to download (default: drive)')
@click.option("--binary", default=True, is_flag=True)
def generate_locations(output_dir, network, binary):
    os.makedirs(output_dir, exist_ok=True)

    cities = {
        "Vienna, Austria": [
            "Innere Stadt", "Leopoldstadt", "Landstraße", "Wieden", "Margareten",
            "Mariahilf", "Neubau", "Josefstadt", "Alsergrund", "Favoriten",
            "Simmering", "Meidling", "Hietzing", "Penzing", "Rudolfsheim-Fünfhaus",
            "Ottakring", "Hernals", "Währing", "Döbling", "Brigittenau",
            "Floridsdorf", "Donaustadt", "Liesing"
        ],
        "New York, USA": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island"],
        "Paris, France": ["1er", "2e", "3e", "4e", "5e"],
        "London, UK": ["Camden", "Kensington and Chelsea"],
        "Berlin, Germany": [
            "Mitte", "Friedrichshain-Kreuzberg", "Pankow",
            "Charlottenburg-Wilmersdorf", "Neukölln"
        ],
        "Amsterdam, Netherlands": ["Centrum", "West", "Zuid", "Oost", "Noord"]
    }

    for city, districts in cities.items():
        for district in districts:
            place = f"{district}, {city}"
            safe_name = place.replace(",", "").replace(" ", "_")
            output_geojson = os.path.join(output_dir, f"{safe_name}.geojson")
            output_csv = os.path.join(output_dir, f"{safe_name}.csv")
            download_street_network(place, network_type=network, output_path=output_geojson)
            segments = extract_segments_from_geojson(output_geojson)
            write_segments_to_csv(segments, output_csv, binary_encode=binary)


if __name__ == "__main__":
    cli()
