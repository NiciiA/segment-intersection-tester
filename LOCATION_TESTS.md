# Location-Based Test Sets

These tests are based on real-world location data from OpenStreetMap, exported using:
- `/generation/street_exporter.py` → to generate **GeoJSON**
- `/generation/street_converter.py` → to convert it into our internal **CSV format**

Each line in the CSV uses the following format:
```
x1;y1:x2;y2
```
Coordinates are stored as 64-bit binary doubles to preserve precision.

## Table of Contents
1. [Vienna Districts](#vienna-districts)
2. [New York Boroughs](#new-york-boroughs)
3. [Paris Arrondissements](#paris-arrondissements)
4. [London Boroughs](#london-boroughs)
5. [Berlin Bezirke](#berlin-bezirke)
6. [Amsterdam Districts](#amsterdam-districts)

---

## Vienna Districts
Tests using real-world data from **Vienna**'s districts. This set evaluates spatial indexing, region boundary intersection, and geographic precision using administrative divisions.

## New York Boroughs
Tests using real-world data from **New York**'s boroughs. This set evaluates spatial indexing, region boundary intersection, and geographic precision using administrative divisions.

## Paris Arrondissements
Tests using real-world data from **Paris**'s arrondissements. This set evaluates spatial indexing, region boundary intersection, and geographic precision using administrative divisions.

## London Boroughs
Tests using real-world data from **London**'s boroughs. This set evaluates spatial indexing, region boundary intersection, and geographic precision using administrative divisions.

## Berlin Bezirke
Tests using real-world data from **Berlin**'s bezirke. This set evaluates spatial indexing, region boundary intersection, and geographic precision using administrative divisions.

## Amsterdam Districts
Tests using real-world data from **Amsterdam**'s districts. This set evaluates spatial indexing, region boundary intersection, and geographic precision using administrative divisions.
