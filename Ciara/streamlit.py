import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurar layout ancho
st.set_page_config(layout="wide")

# Cargar los datos
df = pd.read_csv("Data_Crime_Cleaning.csv")



# Limpiar los datos
df_clean = df[~df['loc_desc'].str.contains('unknown', case=False, na=False)]
df_clean = df_clean[~df_clean['weapon_desc'].str.contains('unknown', case=False, na=False)]

# Filtro: número de elementos a mostrar
top_n = st.slider('¿Cuántos valores quieres mostrar?', min_value=3, max_value=20, value=10)

# Calcular top ubicaciones
top_loc_desc = df_clean['loc_desc'].value_counts().nlargest(top_n)
loc_counts = top_loc_desc.reset_index()
loc_counts.columns = ['Ubicación', 'Frecuencia']

# Calcular top armas
top_weapon_desc = df_clean['weapon_desc'].value_counts().nlargest(top_n)
weapon_counts = top_weapon_desc.reset_index()
weapon_counts.columns = ['Arma', 'Frecuencia']

# Crear márgenes izquierdo y derecho con 35% cada uno, y centro con 30%
left, center, right = st.columns([0.35, 1, 0.35])

# Crear dos columnas para las gráficas lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Lugares más frecuentes de crímenes")
    fig_loc = px.bar(loc_counts, x='Ubicación', y='Frecuencia',
                     title="📍 Lugares más frecuentes de crímenes",
                     color='Frecuencia',
                     labels={'Ubicación': 'Lugar', 'Frecuencia': 'Frecuencia'},
                     template='plotly_dark')
    fig_loc.update_layout(xaxis_tickangle=-45, showlegend=False, height=500)
    st.plotly_chart(fig_loc, use_container_width=True)

with col2:
    st.subheader("🔫 Armas más utilizadas")
    fig_weapon = px.bar(weapon_counts, x='Arma', y='Frecuencia',
                        title="🔫 Armas más utilizadas",
                        color='Frecuencia',
                        labels={'Arma': 'Tipo de Arma', 'Frecuencia': 'Frecuencia'},
                        template='plotly_dark')
    fig_weapon.update_layout(xaxis_tickangle=-45, showlegend=False, height=500)
    st.plotly_chart(fig_weapon, use_container_width=True)


# Línea divisoria
st.markdown("---")

# HEATMAP

# Preparar datos para el heatmap
top_locs = df_clean['loc_desc'].value_counts().nlargest(10).index
top_weapons = df_clean['weapon_desc'].value_counts().nlargest(10).index
df_filtered = df_clean[df_clean['loc_desc'].isin(top_locs) & df_clean['weapon_desc'].isin(top_weapons)]
heatmap_data = pd.crosstab(df_filtered['loc_desc'], df_filtered['weapon_desc'], normalize='columns') * 100

# Crear heatmap con anotaciones
z_vals = heatmap_data.values
x_labels = heatmap_data.columns.tolist()
y_labels = heatmap_data.index.tolist()

fig_heatmap = go.Figure(data=go.Heatmap(
    z=z_vals,
    x=x_labels,
    y=y_labels,
    colorscale='PuBuGn',
    colorbar=dict(title="% en cada arma"),
    zmin=0,
    zmax=100
))

# Anotaciones dentro del heatmap
annotations = []
for i in range(len(y_labels)):
    for j in range(len(x_labels)):
        value = z_vals[i][j]
        annotations.append(
            dict(
                x=x_labels[j],
                y=y_labels[i],
                text=f"{value:.1f}%",
                showarrow=False,
                font=dict(color="white" if value > 50 else "black", size=12)
            )
        )

fig_heatmap.update_layout(
    title='🔥 Distribución de Armas por Ubicación',
    xaxis_title='Tipo de Arma',
    yaxis_title='Ubicación',
    annotations=annotations,
    template='plotly_dark',
    height=600
)

# 🔥 Nueva sección: Gravedad del crimen según arma y ubicación

# Limpieza adicional para gravedad
df_clean = df[
    ~df['loc_desc'].str.contains('unknown', case=False, na=False) &
    ~df['weapon_desc'].str.contains('unknown', case=False, na=False) &
    ~df['crime_severity'].isna()
]

top_weapons = df_clean['weapon_desc'].value_counts().nlargest(10).index
top_locs = df_clean['loc_desc'].value_counts().nlargest(10).index

df_filtered = df_clean[
    df_clean['weapon_desc'].isin(top_weapons) &
    df_clean['loc_desc'].isin(top_locs)
]

# Paleta con solo dos colores
severity_colors = {
    'menos grave': '#2ca02c',    # verde
    'grave': '#d62728'    # rojo
}

# Gravedad por arma
weapon_severity = pd.crosstab(df_filtered['weapon_desc'], df_filtered['crime_severity'], normalize='index') * 100
fig_weapon_sev = go.Figure()
for col in weapon_severity.columns:
    fig_weapon_sev.add_trace(go.Bar(
        x=weapon_severity.index,
        y=weapon_severity[col],
        name=str(col),
        marker=dict(color=severity_colors.get(col, '#cccccc'))  # color por categoría
    ))
fig_weapon_sev.update_layout(
    barmode='stack',
    title='Gravedad del Crimen según Tipo de Arma',
    xaxis_title='Tipo de Arma',
    yaxis_title='% de Casos',
    template='plotly_white',
    xaxis_tickangle=-45,
    height=500
)

# Gravedad por ubicación
loc_severity = pd.crosstab(df_filtered['loc_desc'], df_filtered['crime_severity'], normalize='index') * 100
fig_loc_sev = go.Figure()
for col in loc_severity.columns:
    fig_loc_sev.add_trace(go.Bar(
        x=loc_severity.index,
        y=loc_severity[col],
        name=str(col),
        marker=dict(color=severity_colors.get(col, '#cccccc'))
    ))
fig_loc_sev.update_layout(
    barmode='stack',
    title='Gravedad del Crimen según Ubicación',
    xaxis_title='Ubicación',
    yaxis_title='% de Casos',
    template='plotly_white',
    xaxis_tickangle=-45,
    height=500
)




# Mostrar heatmap
st.plotly_chart(fig_heatmap, use_container_width=True)

# Mostrar gráficas apiladas
col3, col4 = st.columns(2)
with col3:
    st.subheader("📊 Gravedad según arma")
    st.plotly_chart(fig_weapon_sev, use_container_width=True)
with col4:
    st.subheader("📊 Gravedad según ubicación")
    st.plotly_chart(fig_loc_sev, use_container_width=True)


