import json
import folium
import geopandas as gpd
import streamlit as st


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

def extract_points_of_interest(kml_file):
    """
    Extracts points of interest from a KML file.
    """
    gdf = gpd.read_file(kml_file, driver='KML')
    return gdf


def display_points_of_interest(m, gdf):
    """
    Display the points of interest on the Folium map.
    """
    for idx, row in gdf.iterrows():
        folium.Marker([row['geometry'].y, row['geometry'].x], popup=row['name']).add_to(m)