import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")





# Título
st.subheader("Top 10 most common crimes")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Data_Crime_Cleaning.csv")

df = load_data()

# Obtener los 10 delitos más comunes
delitos_comunes = df['crime_desc'].value_counts().head(10)

# Diccionario para renombrar los delitos (puedes modificar según lo que necesites)
nombres_personalizados = {
    'battery - simple assault': 'Simple Assault',
    'burglary from vehicle': 'Burglary from Vehicle',
    'theft of identity': 'Identity Theft',
    'vehicle - stolen': 'Vehicle Theft',
    'theft plain - petty ($950 & under)': 'Petty Theft ($950 & under)',
    'assault with deadly weapon, aggravated assault': 'Aggravated Assault',
    'burglary': 'Burglary',
    'vandalism - felony ($400 & over, all church vandalisms)': 'Felony Vandalism ($400 & over)',
    'theft from motor vehicle - petty ($950 & under)': 'Theft from Vehicle ($950 & under)',
    'intimate partner - simple assault': 'Simple Assault to Intimate Partner'
}

# Renombrar los delitos en el índice
delitos_comunes.index = delitos_comunes.index.to_series().replace(nombres_personalizados)

# Crear gráfico
fig, ax = plt.subplots(figsize=(10, 6))
delitos_comunes.plot(kind='barh', color='darkcyan', ax=ax)
ax.set_xlabel('Reports')
ax.set_ylabel('Crime Description')
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar en Streamlit como imagen (más eficiente)
buf = BytesIO()
fig.savefig(buf, format="png", dpi=100)
st.image(buf)
plt.close(fig)





# Título de la sección
st.subheader("Top 4 most common crimes temporal patterns")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Data_Crime_Cleaning.csv")

df = load_data()

# Asegurar que las fechas estén en formato datetime
df['year_month_ocurrance'] = pd.to_datetime(df['year_month_ocurrance'])

# Diccionario para renombrar los delitos
nombres_personalizados = {
    'vehicle - stolen': 'Vehicle Theft',
    'battery - simple assault': 'Simple Assault',
    'burglary from vehicle': 'Burglary from Vehicle',
    'theft of identity': 'Identity Theft'
}

# Obtener los 4 delitos más comunes
delitos_comunes = df['crime_desc'].value_counts().head(4).index.tolist()

# Preparar gráfico
fig, ax = plt.subplots(figsize=(30, 8))
colores = matplotlib.colormaps['tab10']

# Graficar cada delito
for i, delito in enumerate(delitos_comunes):
    df_filtrado = df[df['crime_desc'].str.contains(delito, case=False, na=False, regex=False)]
    patron = df_filtrado.groupby(df_filtrado['year_month_ocurrance'].dt.to_period('M'))['id_report'].count().sort_index()
    patron.index = patron.index.astype(str)

    # Usar nombre personalizado si existe
    nombre_legenda = nombres_personalizados.get(delito.lower(), delito)
    ax.plot(patron.index, patron.values, marker='o', label=nombre_legenda, color=colores(i))

# Personalización del gráfico
ax.set_xlabel('Date')
ax.set_ylabel('Reports')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
plt.tight_layout()

# Mostrar en Streamlit
buf = BytesIO()
fig.savefig(buf, format="png", dpi=100)
st.image(buf)
plt.close(fig)





# Título de la sección
st.subheader("Time difference between date of occurrence and date reported")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Data_Crime_Cleaning.csv")

df = load_data()

# Asegurar que la columna de diferencia de días exista
if 'dias_diferencia' not in df.columns:
    df['date_ocurrance'] = pd.to_datetime(df['date_ocurrance'])
    df['date_report'] = pd.to_datetime(df['date_report'])
    df['dias_diferencia'] = (df['date_report'] - df['date_ocurrance']).dt.days

# Crear las categorías
conteo_dias = {
    '1 day': (df['dias_diferencia'] == 1).sum(),
    '2-5 days': ((df['dias_diferencia'] >= 2) & (df['dias_diferencia'] <= 5)).sum(),
    '5-20 days': ((df['dias_diferencia'] >= 5) & (df['dias_diferencia'] <= 20)).sum(),
    '20-100 days': ((df['dias_diferencia'] >= 20) & (df['dias_diferencia'] <= 100)).sum(),
    'More than 100 days': (df['dias_diferencia'] > 100).sum()
}

# Crear el gráfico de tarta
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(conteo_dias.values(),
       labels=conteo_dias.keys(),
       autopct='%1.1f%%',
       startangle=140,
       colors=['#66c2a5', '#fc8d62', '#ffd92f', '#8da0cb', '#e78ac3'])

ax.axis('equal')
plt.tight_layout()

# Mostrar gráfico en Streamlit
buf = BytesIO()
fig.savefig(buf, format="png", dpi=100)
st.image(buf)
plt.close(fig)





# Título de la sección
st.subheader("Top 5 crime categories with the longest reporting delays")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Data_Crime_Cleaning.csv")

df = load_data()

# Asegurar que la columna de diferencia de días exista
if 'dias_diferencia' not in df.columns:
    df['date_ocurrance'] = pd.to_datetime(df['date_ocurrance'])
    df['date_report'] = pd.to_datetime(df['date_report'])
    df['dias_diferencia'] = (df['date_report'] - df['date_ocurrance']).dt.days

# Unificar categorías "unknown" y "other crimes"
df['crime_ucr'] = df['crime_ucr'].replace(
    {'unknown': 'Other/Unknown', 'other crimes': 'Other Crimes'}
)

# Calcular el retraso promedio
retraso_por_categoria = df.groupby('crime_ucr')['dias_diferencia'].mean().dropna()

# Obtener las 5 categorías con más retraso
top_categorias_retraso = retraso_por_categoria.sort_values(ascending=False).head(5)

# Renombrar etiquetas para el gráfico
etiquetas_amigables = {
    'aggravated assault': 'Aggravated Assault',
    'vehicle theft': 'Vehicle Theft',
    'burglary': 'Burglary',
    'Other/Unknown': 'Other / Unknown',
    'robbery': 'Robbery'
    # Añade más si fuera necesario
}

# Aplicar los nuevos nombres si existen
labels = [etiquetas_amigables.get(cat, cat.title()) for cat in top_categorias_retraso.index]

# Crear el gráfico de tarta
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(top_categorias_retraso.values,
       labels=labels,
       autopct='%1.1f%%',
       startangle=140,
       colors=plt.colormaps['Set3'].colors[:5])
ax.axis('equal')
plt.tight_layout()

# Mostrar en Streamlit
buf = BytesIO()
fig.savefig(buf, format="png", dpi=100)
st.image(buf)
plt.close(fig)