from geopy.distance import geodesic
import gpxpy
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

import plotly.graph_objects as go


def plot_altitude_profile(file_path):
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)

    data = []
    # Get the track points from the GPX file
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.elevation, point.time, point.latitude, point.longitude])

    # Create a DataFrame from all segment points
    df = pd.DataFrame(data, columns=['Altitude', 'Time', 'Latitude', 'Longitude'])

    # Calculate cumulative distance
    df['Distance'] = 0
    for i in range(1, len(df)):
        df.loc[i, 'Distance'] = geodesic((df.loc[i-1, 'Latitude'], df.loc[i-1, 'Longitude']), (df.loc[i, 'Latitude'], df.loc[i, 'Longitude'])).km

    df['CumulativeDistance'] = df['Distance'].cumsum()

    # Replace infinite values with NaN and drop rows with missing altitude values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=['Altitude'])

    # Find the peak altitude and its corresponding distance
    peak_altitude = df['Altitude'].max()
    peak_distance = df.loc[df['Altitude'].idxmax(), 'CumulativeDistance']

    # Plot the altitude profile using plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['CumulativeDistance'], y=df['Altitude'], name='Altitude',
                             line=dict(color='firebrick', width=4)))

    # Add peak annotation
    fig.add_annotation(
        x=peak_distance,
        y=peak_altitude,
        text="Peak",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
    )

    # Update the layout
    fig.update_layout(title='Altitude Profile', xaxis_title='Distance (km)', yaxis_title='Altitude (m)')

    st.plotly_chart(fig)

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
