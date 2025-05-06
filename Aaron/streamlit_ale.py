import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import gdown
import geopandas as gpd
from folium import FeatureGroup, LayerControl
import pydeck as pdk
# Título de la app
st.title("Crime Location")

# Cargar datos
df = pd.read_csv('Data_Crime_Cleaning.csv')

# # Mostrar las primeras filas si quieres
# st.write("Primeras filas del dataset:")
# st.dataframe(df.head(10))



#-----------------------------------------------------------------------------------------------

# urlgeo = 'https://drive.google.com/file/d/18QOLtJBH00qtzGlF3muy18VvqojZp7Ul/view?usp=drive_link'

# outputgeo = 'LAPD_Division_5922489107755548254.geojson'

# gdown.download(urlgeo, outputgeo, quiet=False, fuzzy=True)

# gdf = gpd.read_file(outputgeo)  # Ajusta la ruta si es necesario



# # Diccionario para mapear tus nombres a los del GeoJSON
# area_name_mapping = {
#     '77th street': '77TH STREET',
#     'central': 'CENTRAL',
#     'devonshire': 'DEVONSHIRE',
#     'foothill': 'FOOTHILL',
#     'harbor': 'HARBOR',
#     'hollenbeck': 'HOLLENBECK',
#     'hollywood': 'HOLLYWOOD',
#     'mission': 'MISSION',
#     'n hollywood': 'NORTH HOLLYWOOD'
# }

# # Crear nueva columna normalizada y mapear a nombres del GeoJSON
# df['area_name_clean'] = df['area_name'].str.lower().map(area_name_mapping)

# # Agrupar crímenes por área y severidad
# crime_counts = df.groupby(['area_name_clean', 'crime_severity']).size().unstack(fill_value=0).reset_index()

# # Unir con el GeoDataFrame por el nombre de la zona
# choropleth_df = gdf.merge(crime_counts, left_on='APREC', right_on='area_name_clean')



# # ---------------------------------------------------------------------------------------


# # 1. Filtrar registros con raza válida
df_race = df[df['descent_victim'] != '-']

# # 2. Top 5 razas (sin '-')
# top_races = df_race['descent_victim'].value_counts().head(5).index.tolist()

# # 3. Asignar colores
# race_colors = {
#     top_races[0]: 'blue',
#     top_races[1]: 'green',
#     top_races[2]: 'red',
#     top_races[3]: 'orange',
#     top_races[4]: 'purple',
# }

# # 4. Crear mapa base
# m = folium.Map(location=[34.05, -118.25], zoom_start=11, tiles='cartodbpositron')

# # 5. Añadir puntos por raza
# for race, color in race_colors.items():
#     fg = FeatureGroup(name=f'Raza: {race}')
#     subset = df_race[df_race['descent_victim'] == race].dropna(subset=['latitude', 'longitude']).head(500)
#     for _, row in subset.iterrows():
#         folium.CircleMarker(
#             location=[row['latitude'], row['longitude']],
#             radius=2,
#             color=color,
#             fill=True,
#             fill_color=color,
#             fill_opacity=0.5,
#             popup=f"Raza: {race} | Zona: {row['area_name']}"
#         ).add_to(fg)
#     fg.add_to(m)

# # 6. Control de capas
# LayerControl().add_to(m)

# st.header("Mapa de crímenes por raza en Los Ángeles", divider = "orange")
# st.markdown("""
#     <style>
#         .main {
#             padding-top: 0rem;
#             padding-bottom: 0rem;
#         }
#         .block-container {
#             padding: 0 !important;
#         }
#         iframe {
#             height: 100vh !important;
#         }
#     </style>
# """, unsafe_allow_html=True)
# st_data = st_folium(m, use_container_width=True)

# -------------------------------------------------------------------------------------------------------------
st.header("CrimeSeverityAreaI", divider ="orange")
st.image("1_CrimeSeverityAreaII.png")

# -------------------------------------------------------------------------------------------------------------
st.header("CrimeSeverityAreaI", divider ="orange")
st.image("2_CrimeTypebyAreaI.png")

# -------------------------------------------------------------------------------------------------------------
st.header("Heatmap I", divider ="orange")
st.image('heatmap1.png')

# -----------------------------------------

st.header("Count by Location", divider ="orange")

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=34.05,
            longitude=-118.25,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df_race.head(10000),
                get_position="[longitude, latitude]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=df_race.head(1000),
                get_position="[longitude, latitude]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)
# -------------------------------------------------------------------------------------------------------------

st.header("Heatmap II", divider ="orange")
st.image("4_HeatmapII.png")

# -------------------------------------------------------------------------------------------------------------

st.header("Heatmap III", divider ="orange")
st.image("5_HeatMapIII.png")

# -------------------------------------------------------------------------------------------------------------
st.header("HeatMap by Crime Stolen Cars", divider ="orange")
st.image("6_HeatMapbyCrime_StolenCarsIIII.png")

# -------------------------------------------------------------------------------------------------------------
st.header("Modus Operandis by Crime Type Sexual.", divider ="orange")
st.image("7_MO_by Crime Type_Sexual.png")

# -------------------------------------------------------------------------------------------------------------

