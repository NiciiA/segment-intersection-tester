# Location-Based Test Sets

These tests are based on real-world location data from OpenStreetMap, exported using:
- `/generation/street_exporter.py` → to generate **GeoJSON**
- `/generation/street_converter.py` → to convert it into our internal **CSV format**

Each line in the CSV uses the following format:
```
x1;y1:x2;y2
```
Coordinates are stored as 64-bit binary doubles to guaranty consistency throughout all implementations.

The test data is also:
- **Randomized** in segment length using `/utils/length_randomizer.py`
- **Shuffled** in order using `/utils/line_shuffler.py`

## Table of Contents
1. [Vienna Districts](#vienna-districts)
2. [New York Boroughs](#new-york-boroughs)
3. [Paris Arrondissements](#paris-arrondissements)
4. [London Boroughs](#london-boroughs)
5. [Berlin Bezirke](#berlin-bezirke)
6. [Amsterdam Districts](#amsterdam-districts)

---

## Vienna  
Innere Stadt, Leopoldstadt, Landstraße, Wieden, Margareten, Mariahilf, Neubau, Josefstadt, Alsergrund, Favoriten, Simmering, Meidling, Hietzing, Penzing, Rudolfsheim-Fünfhaus, Ottakring, Hernals, Währing, Döbling, Brigittenau, Floridsdorf, Donaustadt, Liesing

## New York  
Manhattan, Brooklyn, Queens, The Bronx, Staten Island

## Paris  
1er, 2e, 3e, 4e, 5e

## London  
Camden, Kensington and Chelsea

## Berlin  
Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf, Neukölln

## Amsterdam  
Centrum, West, Zuid, Oost, Noord
