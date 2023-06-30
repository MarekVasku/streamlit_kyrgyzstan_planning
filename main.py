import streamlit as st
from src.map_data_processing import plot_altitude_profile, plot_gpx_track, gpx_to_dataframe
import pathlib as Path
import pandas as pd


import warnings
warnings.filterwarnings('ignore')


def main():
    st.title('Kyrgyzstan Trip Planning')

    st.write("""
    Welcome to the Kyrgyzstan trip planning application. 
    This app will provide interactive maps and charts to help you plan your adventure in Kyrgyzstan!
    """)

    mapbox_api_token = 'pk.eyJ1IjoibWFyZWt2YXNrdSIsImEiOiJja2trZTc0NHIwcGx5MndzN25idmJsanpuIn0.-fgkhjZNAzYg1OUw82ieZw'


    # Define the data directory and the GPX files
    data_dir = Path.Path('data')
    gpx_files = list(data_dir.glob('*.gpx'))

    # Let's assume that the first two GPX files are your journeys
    journeys = gpx_files[:2]

    # And the last two GPX files are your treks
    treks = gpx_files[2:]

    # You can then select a file and display the altitude profile
    selected_file = st.selectbox('Select a journey/trek', gpx_files)
    fig = plot_altitude_profile(selected_file)
    st.pyplot(fig)

    # Embed the iframe
    iframe_html = '<iframe style="border:none" src="https://en.frame.mapy.cz/s/pevafekofa" width="500" height="333" frameborder="0"></iframe>'
    st.components.v1.html(iframe_html, height=400)

    # Plot the track on a map
    gpx_df = gpx_to_dataframe(selected_file)
    if not gpx_df.empty:
        plot_gpx_track(gpx_df, mapbox_api_token)


    st.write("""
    Happy adventuring!
    """)


if __name__ == '__main__':
    main()
