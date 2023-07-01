import streamlit as st
from src.map_data_processing import plot_altitude_profile, plot_gpx_track, gpx_to_dataframe
from src.helper_functions import add_marker, load_map_links, get_trip_names, \
      extract_points_of_interest, display_points_of_interest
import pathlib as Path
import folium
from streamlit_folium import folium_static

import warnings
warnings.filterwarnings('ignore')


def main():
    st.title('Kyrgyzstan expedice - plánování')

    # Add the Kyrgyzstan flag image on the left side
    col1 = st.sidebar
    kyrgyzstan_flag_pic = 'images/Flag_of_Kyrgyzstan.png'
    col1.image(kyrgyzstan_flag_pic, use_column_width=True)

    # Add the Ala Kul lake image on the right side
    col2 = st.empty()
    ala_kul_lake_pic = 'images/ala_kul_lake.jpg'
    col2.image(ala_kul_lake_pic, caption='jezero Ala Kul', use_column_width=True)

    st.write("""
    Welcome to the Kyrgyzstan trip planning application. 
    This app will provide interactive maps and charts to help you plan your adventure in Kyrgyzstan!
    """)

    print('Comment')
    mapbox_api_token = 'pk.eyJ1IjoibWFyZWt2YXNrdSIsImEiOiJja2trZTc0NHIwcGx5MndzN25idmJsanpuIn0.-fgkhjZNAzYg1OUw82ieZw'

    # Create a folium map
    m = folium.Map(location=[41.2044, 74.7661], zoom_start=7)

    # Display the points of interest on the map
    csv_file = 'data/POI Kyrgyzstan.csv'
    points_of_interest = extract_points_of_interest(csv_file)
    display_points_of_interest(m, points_of_interest)

    # Display the map
    folium_static(m)

    # Load the iframe links
    map_links = load_map_links('data/mapycz_links.json')

    # Define the data directory and the GPX files
    data_dir = Path.Path('data')
    gpx_files = list(data_dir.glob('*.gpx'))

    # Extract file names without extensions
    trip_names = get_trip_names(gpx_files)

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