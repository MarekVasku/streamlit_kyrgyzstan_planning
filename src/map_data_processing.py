from geopy.distance import geodesic
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns


def plot_altitude_profile(file_path):
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)

    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.elevation, point.time, point.latitude, point.longitude])

    df = pd.DataFrame(data, columns=['Altitude', 'Time', 'Latitude', 'Longitude'])

    # Calculate cumulative distance
    df['Distance'] = 0
    for i in range(1, len(df)):
        df.loc[i, 'Distance'] = geodesic((df.loc[i-1, 'Latitude'], df.loc[i-1, 'Longitude']),
                                         (df.loc[i, 'Latitude'], df.loc[i, 'Longitude'])).km

    df['CumulativeDistance'] = df['Distance'].cumsum()

    # Plot the altitude profile
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='CumulativeDistance', y='Altitude', color='blue')

    # Add labels and title
    plt.xlabel('Distance (km)')
    plt.ylabel('Altitude (m)')
    plt.title('Altitude Profile - Mountain Trek')

    # Add grid lines and background color
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.axhspan(0, max(df['Altitude']), facecolor='lightgray', alpha=0.2)

    # Add markers for key points
    peaks = df.loc[df['Altitude'].idxmax(), ['CumulativeDistance', 'Altitude']]
    plt.scatter(x=peaks['CumulativeDistance'], y=peaks['Altitude'], color='red', label='Peaks')

    # Customize the plot style
    sns.set_style('whitegrid')
    sns.despine()

    # Show legend
    plt.legend()

    return plt.gcf()


def plot_gpx_track(gpx_df, mapbox_api_token):
    fig_map = px.line_mapbox(gpx_df, lat='latitude', lon='longitude', hover_name=gpx_df.index, zoom=10,
                             mapbox_style="outdoors", color_discrete_sequence=['red'], width=800, height=600)
    fig_map.update_traces(line=dict(width=3))
    fig_map.update_layout(mapbox={'accesstoken': mapbox_api_token}, width=800, height=600)
    st.plotly_chart(fig_map)


def gpx_to_dataframe(gpx_file_path):
    """
    Converts GPX file into DataFrame
    """
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.latitude, point.longitude, point.elevation])

    return pd.DataFrame(data, columns=['latitude', 'longitude', 'altitude'])
