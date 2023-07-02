import streamlit as st
from src.map_data_processing import plot_altitude_profile, plot_gpx_track, gpx_to_dataframe
from src.helper_functions import add_marker, load_map_links, get_trip_names, \
      extract_points_of_interest, display_points_of_interest
import pathlib as Path
import folium
import streamlit_folium

from streamlit_folium import folium_static
import pandas as pd
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings('ignore')


def main():
    st.title('Kyrgyzstan expedice, září 2023 - plánování')
    st.markdown('<h2 style="text-align: center">mapy a grafy</h2>', unsafe_allow_html=True)


    col1 = st.sidebar
    kyrgyzstan_flag_pic = 'images/Flag_of_Kyrgyzstan.png'
    col1.image(kyrgyzstan_flag_pic, use_column_width=True)

    # Read itinerary.csv
    df_itinerary = pd.read_csv('data/itinerary.csv')
    st.sidebar.table(df_itinerary)

    col2 = st.empty()
    ala_kul_lake_pic = 'images/ala_kul_lake.jpg'
    col2.image(ala_kul_lake_pic, caption='jezero Ala Kul', use_column_width=True)

    st.markdown('<h3 style="text-align: center">Vybrané místa</h3>', unsafe_allow_html=True)
    st.write("""
    Toto sou spíš jen výsledky googlení některé ty věci. Feel free to googlit a nacházet víc věcí ale hlavně v oblasti
    Karakolu a Ala-Archa pod Biškekem.
    """)

    mapbox_api_token = 'pk.eyJ1IjoibWFyZWt2YXNrdSIsImEiOiJja2trZTc0NHIwcGx5MndzN25idmJsanpuIn0.-fgkhjZNAzYg1OUw82ieZw'

    # Create a folium map with 'openstreetmap' as the base layer
    m = folium.Map(location=[41.2044, 74.7661], zoom_start=7, tiles='OpenStreetMap')

    # Display the points of interest on the map
    csv_file = 'data/POI Kyrgyzstan.csv'
    points_of_interest = extract_points_of_interest(csv_file)
    display_points_of_interest(m, points_of_interest)

    # Add tiles to map
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)

    # Create a layer control and add it to the map
    layer_control = folium.LayerControl()
    layer_control.add_to(m)

    # Display the map
    folium_static(m)

    # Load the iframe links
    map_links = load_map_links('data/mapycz_links.json')
    # Define the data directory and the GPX files
    data_dir = Path.Path('data')
    gpx_files = list(data_dir.glob('*.gpx'))

    trip_dict = {
        "ala_kul_trek": "TREK: Ala-Kul trek",
        "pik_uchytel": "TREK: Výstup na Pik Uchytel",
        "airport_bishkek": "PŘESUN: z letiště do Biškeku (maršrutka)",
        "bishkek_karakol": "PŘESUN: Biškek - Karakol (maršrutka)"
    }

    # Extract file names without extensions
    trip_names = [file.stem for file in gpx_files]

    # Create two lists for Trek and Marshrutka rides
    trek_trips = [trip_dict[name] for name in trip_names if name in trip_dict and 'TREK' in trip_dict[name]]
    marshrutka_trips = [trip_dict[name] for name in trip_names if name in trip_dict and 'PŘESUN' in trip_dict[name]]

    st.markdown('<h3 style="text-align: center">Vizualizace treků a přesunů</h3>', unsafe_allow_html=True)

    # Create a selection box with the user-friendly trip names
    selected_trip = st.selectbox('Zvol trek nebo přesun', trek_trips + marshrutka_trips)

    # Get the path to the GPX file of the selected trip
    selected_trip_filename = next((name for name, friendly_name in trip_dict.items() if friendly_name == selected_trip),
                                  None)
    selected_gpx_path = next((file for file in gpx_files if file.stem == selected_trip_filename), None)

    if selected_trip_filename and selected_gpx_path:
        gpx_df = gpx_to_dataframe(selected_gpx_path)
        if not gpx_df.empty:
            plot_gpx_track(gpx_df, mapbox_api_token, color='blue' if 'maršrutka' in selected_trip else 'red')

        if 'maršrutka' not in selected_trip:
            plot_altitude_profile(selected_gpx_path)

        selected_map_html = map_links.get(selected_trip_filename)
        if selected_map_html:
            selected_map_html = selected_map_html.replace('width="500"', 'width="800"').replace('height="333"',
                                                                                                'height="600"')
            st.components.v1.html(selected_map_html, height=400)

            # Extract the 'src' link and display it as a clickable hyperlink
            soup = BeautifulSoup(selected_map_html, 'html.parser')
            map_link = soup.iframe['src']
            st.markdown(f"[Tady je přímo ten odkaz na Mapy.cz]({map_link})")
        else:
            st.write("Mapy.cz vložené okno nepřiloženo, šak je to jen cesta.")
    else:
        st.write("Zvol validní výlet.")

    st.write("""
                Мен жылкынын сүтүн спирт менен аралаштырмакмын
                """)


if __name__ == '__main__':
    main()