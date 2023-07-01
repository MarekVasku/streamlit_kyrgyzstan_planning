import streamlit as st
from src.map_data_processing import plot_altitude_profile, plot_gpx_track, gpx_to_dataframe
import pathlib as Path
import json

import warnings
warnings.filterwarnings('ignore')

def main():
    st.title('Kyrgyzstan Trip Planning')

    st.write("""
    Welcome to the Kyrgyzstan trip planning application. 
    This app will provide interactive maps and charts to help you plan your adventure in Kyrgyzstan!
    """)

    print('Comment')
    mapbox_api_token = 'pk.eyJ1IjoibWFyZWt2YXNrdSIsImEiOiJja2trZTc0NHIwcGx5MndzN25idmJsanpuIn0.-fgkhjZNAzYg1OUw82ieZw'

    # Load the iframe links
    with open('data/mapycz_links.json', 'r') as file:
        map_links = json.load(file)

    # Define the data directory and the GPX files
    data_dir = Path.Path('data')
    gpx_files = list(data_dir.glob('*.gpx'))

    # Extract file names without extensions
    trip_names = [file.stem for file in gpx_files]

    # Create a selection box with the trip names
    selected_trip = st.selectbox('Select a trip', trip_names)


    # Get the path to the GPX file of the selected trip
    selected_gpx_path = next((file for file in gpx_files if file.stem == selected_trip), None)

    if selected_gpx_path:
        # Display the mapbox map
        gpx_df = gpx_to_dataframe(selected_gpx_path)
        if not gpx_df.empty:
            plot_gpx_track(gpx_df, mapbox_api_token)

        # Display the altitude profile
        fig = plot_altitude_profile(selected_gpx_path)
        st.pyplot(fig)

    # Get the iframe HTML of the selected map
    selected_map_html = map_links.get(selected_trip)

    # Display the selected map if exists
    if selected_map_html:
        selected_map_html = selected_map_html.replace('width="500"', 'width="800"').replace('height="333"',
                                                                                            'height="600"')
        st.components.v1.html(selected_map_html, height=400)
    else:
        st.write("No embedded map available for this selection.")

    st.write("""
    Happy adventuring!
    """)


if __name__ == '__main__':
    main()