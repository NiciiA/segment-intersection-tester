import osmnx as ox
import argparse


def download_street_network(place: str, network_type: str = 'drive', output_path: str = 'streets.geojson'):
    """Download and save a street network GeoJSON from a place name."""
    print(f"Downloading '{network_type}' network for: {place}")
    G = ox.graph_from_place(place, network_type=network_type)
    edges = ox.graph_to_gdfs(G, nodes=False)
    edges.to_file(output_path, driver='GeoJSON')
    print(f"Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Download a street network as GeoJSON using OSMnx.")
    parser.add_argument(
        '-p', '--place',
        type=str,
        default='Innere Stadt, Vienna, Austria',
        help='Place name to query (e.g. "Innere Stadt, Vienna, Austria")')
    parser.add_argument(
        '-n', '--network',
        type=str,
        default='drive',
        choices=['drive', 'walk', 'bike', 'all', 'all_private'],
        help='Type of network to download (default: drive)')
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='streets.geojson',
        help='Output file name (default: streets.geojson)')

    args = parser.parse_args()
    download_street_network(args.place, args.network, args.output)


if __name__ == "__main__":
    main()
