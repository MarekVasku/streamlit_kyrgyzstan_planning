import json
import folium
import streamlit as st
import csv
import pandas as pd


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



def extract_points_of_interest(csv_file):
    """
    Extracts points of interest from a CSV file and returns a DataFrame.
    """
    points_of_interest = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            wkt = row['WKT']
            name = row['Name']
            category = row['Category']
            description = row['Description']

            # Extract the coordinates from the WKT string
            coordinates = wkt.strip('POINT ()').split(' ')
            longitude = float(coordinates[0])
            latitude = float(coordinates[1])

            points_of_interest.append((name, latitude, longitude, category, description))

    # Create a DataFrame from the list of points of interest
    df = pd.DataFrame(points_of_interest, columns=['Name', 'Latitude', 'Longitude', 'Category', 'Description'])
    return df


def display_points_of_interest(m, gdf):
    """
    Display points of interest on a Folium map.
    """
    category_colors = {
        "Město": "blue",
        "Příroda": "green",
        "Treky": "red",
    }

    unique_categories = gdf['Category'].unique().tolist()

    for category in unique_categories:
        feature_group = folium.FeatureGroup(name=category)

        rows = gdf[gdf['Category'] == category]

        for idx, row in rows.iterrows():
            color = category_colors.get(row['Category'], 'black')
            html = f"<b>{row['Name']}</b><br><span style='color: {color};'>{row['Category']}</span><br>{row['Description']}"
            iframe = folium.IFrame(html, width=200, height=100)
            popup = folium.Popup(iframe, max_width=200)
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                popup=popup,
                icon=folium.Icon(color=color)
            ).add_to(feature_group)

        feature_group.add_to(m)

    # Add a layer control to toggle feature groups
    folium.LayerControl().add_to(m)



