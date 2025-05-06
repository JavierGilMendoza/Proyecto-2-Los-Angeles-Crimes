import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Función para centrar imagen
def mostrar_imagen_centrada(buf):
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

# Página principal
st.title("Temporal patterns")

# Título
st.header("Top 10 most common crimes", divider="orange")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Data_Crime_Cleaning.csv")

df = load_data()

# Obtener los 10 delitos más comunes
delitos_comunes = df['crime_desc'].value_counts().head(10)

# Diccionario para renombrar
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
delitos_comunes.index = delitos_comunes.index.to_series().replace(nombres_personalizados)

# Crear gráfico
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
delitos_comunes.plot(kind='barh', color='darkcyan', ax=ax)
ax.set_xlabel('Reports', color='white')
ax.set_ylabel('Crime Description', color='white')
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
plt.tight_layout()

# Guardar y mostrar
buf = BytesIO()
fig.savefig(buf, format="png", dpi=100, transparent=True)
buf.seek(0)
mostrar_imagen_centrada(buf)
plt.close(fig)

# -------------------------------

st.header("Top 4 most common crimes temporal patterns", divider="orange")

df = load_data()
df['year_month_ocurrance'] = pd.to_datetime(df['year_month_ocurrance'])

nombres_personalizados = {
    'vehicle - stolen': 'Vehicle Theft',
    'battery - simple assault': 'Simple Assault',
    'burglary from vehicle': 'Burglary from Vehicle',
    'theft of identity': 'Identity Theft'
}

delitos_comunes = df['crime_desc'].value_counts().head(4).index.tolist()

fig, ax = plt.subplots(figsize=(30, 8))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
colores = matplotlib.colormaps['tab10']

for i, delito in enumerate(delitos_comunes):
    df_filtrado = df[df['crime_desc'].str.contains(delito, case=False, na=False, regex=False)]
    patron = df_filtrado.groupby(df_filtrado['year_month_ocurrance'].dt.to_period('M'))['id_report'].count().sort_index()
    patron.index = patron.index.astype(str)
    nombre_legenda = nombres_personalizados.get(delito.lower(), delito)
    ax.plot(patron.index, patron.values, marker='o', label=nombre_legenda, color=colores(i))

ax.set_xlabel('Date')
ax.set_ylabel('Reports')
ax.tick_params(axis='x', rotation=45, colors='white')
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
plt.tight_layout()

buf = BytesIO()
fig.savefig(buf, format="png", dpi=100)
buf.seek(0)
mostrar_imagen_centrada(buf)
plt.close(fig)

# -------------------------------

st.header("Time difference between date of occurrence and date reported", divider="orange")

df = load_data()
if 'dias_diferencia' not in df.columns:
    df['date_ocurrance'] = pd.to_datetime(df['date_ocurrance'])
    df['date_report'] = pd.to_datetime(df['date_report'])
    df['dias_diferencia'] = (df['date_report'] - df['date_ocurrance']).dt.days

conteo_dias = {
    '1 day': (df['dias_diferencia'] == 1).sum(),
    '2-5 days': ((df['dias_diferencia'] >= 2) & (df['dias_diferencia'] <= 5)).sum(),
    '5-20 days': ((df['dias_diferencia'] >= 5) & (df['dias_diferencia'] <= 20)).sum(),
    '20-100 days': ((df['dias_diferencia'] >= 20) & (df['dias_diferencia'] <= 100)).sum(),
    'More than 100 days': (df['dias_diferencia'] > 100).sum()
}

fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

wedges, texts, autotexts = ax.pie(
    conteo_dias.values(),
    labels=conteo_dias.keys(),
    autopct='%1.1f%%',
    startangle=140,
    colors=['#66c2a5', '#fc8d62', '#ffd92f', '#8da0cb', '#e78ac3']
)

for text in texts:
    text.set_color('white')
for autotext in autotexts:
    autotext.set_color('white')

ax.axis('equal')
plt.tight_layout()

buf = BytesIO()
fig.savefig(buf, format="png", dpi=100, transparent=True)
buf.seek(0)
mostrar_imagen_centrada(buf)
plt.close(fig)

# -------------------------------

st.header("Top 5 crime categories with the longest reporting delays", divider="orange")

df = load_data()
if 'dias_diferencia' not in df.columns:
    df['date_ocurrance'] = pd.to_datetime(df['date_ocurrance'])
    df['date_report'] = pd.to_datetime(df['date_report'])
    df['dias_diferencia'] = (df['date_report'] - df['date_ocurrance']).dt.days

df['crime_ucr'] = df['crime_ucr'].replace(
    {'unknown': 'Other/Unknown', 'other crimes': 'Other Crimes'}
)

retraso_por_categoria = df.groupby('crime_ucr')['dias_diferencia'].mean().dropna()
top_categorias_retraso = retraso_por_categoria.sort_values(ascending=False).head(5)

etiquetas_amigables = {
    'aggravated assault': 'Aggravated Assault',
    'vehicle theft': 'Vehicle Theft',
    'burglary': 'Burglary',
    'Other/Unknown': 'Other / Unknown',
    'robbery': 'Robbery'
}

labels = [etiquetas_amigables.get(cat, cat.title()) for cat in top_categorias_retraso.index]

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    top_categorias_retraso.values,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colores
)

for i, (text, autotext, label) in enumerate(zip(texts, autotexts, labels)):
    text.set_color('white')  # Nombre de categoría
    if label == 'Financial Crime':
        autotext.set_color('black')  # Porcentaje en negro
    else:
        autotext.set_color('white')

ax.axis('equal')
plt.tight_layout()

buf = BytesIO()
fig.savefig(buf, format="png", dpi=100, transparent=True)
buf.seek(0)
mostrar_imagen_centrada(buf)
plt.close(fig)
