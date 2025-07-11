import subprocess
import os

def run_export(place, output_file, network="drive"):
    print(f"Exporting: {place} -> {output_file}")
    subprocess.run([
        "python", "street_exporter.py",
        "-p", place,
        "-n", network,
        "-o", output_file
    ], check=True)

def main():
    base_output_dir = "exports"
    os.makedirs(base_output_dir, exist_ok=True)

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
            output_path = os.path.join(base_output_dir, f"{safe_name}.geojson")
            run_export(place, output_path)

if __name__ == "__main__":
    main()
