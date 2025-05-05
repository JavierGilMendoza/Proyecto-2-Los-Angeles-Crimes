import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Título de la app
st.title("Mapa de Calor de Crímenes")

# Cargar datos
df = pd.read_csv('Data_Crime_Cleaning.csv')

# Mostrar las primeras filas si quieres
st.write("Primeras filas del dataset:")
st.dataframe(df.head(10))

# Crear el mapa
mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=11)

# Preparar datos para el HeatMap
heat_data = df[['latitude', 'longitude']].dropna().values.tolist()

# Añadir capa de calor
HeatMap(heat_data, radius=10).add_to(mapa)

# Mostrar el mapa en Streamlit
st.subheader("Mapa de calor")
st_folium(mapa, width=700, height=500)

