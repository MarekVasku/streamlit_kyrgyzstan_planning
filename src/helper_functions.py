import json
import folium
import streamlit as st
import csv


def add_marker(map, name, latitude, longitude):
    """
    Add a marker to a folium map.
    """
    folium.Marker([latitude, longitude], popup=name).add_to(map)


def load_map_links(filepath):
    """
    Load iframe links from a JSON file.
    """
    with open(filepath, 'r') as file:
        map_links = json.load(file)
    return map_links


def get_trip_names(gpx_files):
    """
    Extract file names without extensions from a list of GPX files.
    """
    trip_names = [file.stem for file in gpx_files]
    return trip_names


def display_map(html):
    """
    Display the selected map HTML code.
    """
    html = html.replace('width="500"', 'width="800"').replace('height="333"', 'height="600"')
    folium.Element(html).add_to(folium.Map())


def display_message(message):
    """
    Display a message using Streamlit.
    """
    st.write(message)


import pandas as pd

def extract_points_of_interest(csv_file):
    """
    Extracts points of interest from a CSV file and returns a DataFrame.
    """
    points_of_interest = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            wkt = row['WKT']
            name = row['name']
            description = row['description']

            # Extract the coordinates from the WKT string
            coordinates = wkt.strip('POINT ()').split(' ')
            x = float(coordinates[0])
            y = float(coordinates[1])

            points_of_interest.append((name, x, y, description))

    # Create a DataFrame from the list of points of interest
    df = pd.DataFrame(points_of_interest, columns=['name', 'x', 'y', 'description'])
    return df


def display_points_of_interest(m, gdf):
    """
    Display points of interest on a Folium map.
    """
    for idx, row in gdf.iterrows():
        folium.Marker([row['y'], row['x']], popup=row['name']).add_to(m)

