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
    fig.add_trace(go.Scatter(
        x=df['CumulativeDistance'],
        y=df['Altitude'],
        name='Altitude',
        line=dict(color='firebrick', width=4),
        hovertemplate=
        '<b>Nadmořská výška</b>: %{y:.2f} m n. m.' +
        '<br><b>Vzdálenost</b>: %{x:.2f} km<extra></extra>',
    ))

    # Add peak annotation
    fig.add_annotation(
        x=peak_distance,
        y=peak_altitude,
        text="Vrchol",
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

    fig.update_layout(title='Výškový profil', xaxis_title='Vzdálenost (km)', yaxis_title='Nadmořská výška (m n. m.)')

    st.plotly_chart(fig)


def plot_gpx_track(gpx_df, mapbox_api_token, color='blue'):
    fig = px.line_mapbox(gpx_df, lat="latitude", lon="longitude",  color_discrete_sequence=[color], zoom=10, height=300, hover_data=["altitude"])

    center_lat = gpx_df.latitude.mean()
    center_lon = gpx_df.longitude.mean()

    fig.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_accesstoken=mapbox_api_token,
        mapbox_zoom=10,
        mapbox_center_lat = center_lat,
        mapbox_center_lon = center_lon,
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)




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
