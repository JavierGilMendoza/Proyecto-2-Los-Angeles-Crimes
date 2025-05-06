import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurar layout ancho
# st.set_page_config(layout="wide")

st.title("Weapon Study")

# Cargar los datos
df = pd.read_csv("Data_Crime_Cleaning.csv")



# Limpiar los datos
df_clean = df[~df['loc_desc'].str.contains('unknown', case=False, na=False)]
df_clean = df_clean[~df_clean['weapon_desc'].str.contains('unknown', case=False, na=False)]

# Filtro: número de elementos a mostrar
top_n = st.slider('Values to show', min_value=3, max_value=20, value=10)

# Calcular top ubicaciones
top_loc_desc = df_clean['loc_desc'].value_counts().nlargest(top_n)
loc_counts = top_loc_desc.reset_index()
loc_counts.columns = ['Ubicación', 'Frecuency']

# Calcular top armas
top_weapon_desc = df_clean['weapon_desc'].value_counts().nlargest(top_n)
weapon_counts = top_weapon_desc.reset_index()
weapon_counts.columns = ['Arma', 'Frecuency']

# Crear márgenes izquierdo y derecho con 35% cada uno, y centro con 30%
left, center, right = st.columns([0.35, 1, 0.35])

# Crear dos columnas para las gráficas lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Most common crime places")
    fig_loc = px.bar(
        loc_counts,
        x='Ubicación',
        y='Frecuency',
        color='Frecuency',
        labels={'Ubicación': 'Place', 'Frecuency': 'Frecuency'},
        template='plotly_dark'
    )
    fig_loc.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Texto general (título, etiquetas, etc.)
    xaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    )
)

    st.plotly_chart(fig_loc, use_container_width=True)


with col2:
    st.subheader("Most used weapons")
    fig_weapon = px.bar(
    weapon_counts,
    x='Arma',
    y='Frecuency',
    color='Frecuency',
    labels={'Arma': 'Type of weapon', 'Frecuency': 'Frecuency'},
    template='plotly_dark'
)
    fig_weapon.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
    height=560,
    paper_bgcolor='rgba(0,0,0,0)',  # Fondo exterior transparente
    plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),  # Texto general (título, etiquetas, etc.)
    xaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    )    # Fondo del área del gráfico transparente
)
    st.plotly_chart(fig_weapon, use_container_width=True)



# Línea divisoria
st.divider()

# HEATMAP
st.header("Weapons Distribution by Location", divider = "orange")
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
    colorbar=dict(title="% in each weapon"),
    zmin=0,
    zmax=100
))
fig_heatmap.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',  # Fondo exterior transparente
    plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),  # Texto general (título, etiquetas, etc.)
    xaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    )
)

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
    xaxis_title='Type of weapon',
    yaxis_title='Ubication',
    annotations=annotations,
    template='plotly_dark',
    height=600
)

# Nueva sección: Gravedad del crimen según arma y ubicación

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
    font=dict(color='white'),
    barmode='stack',
    xaxis_title='Type of weapon',
    yaxis_title='% of cases',
    template='plotly_white',
    xaxis_tickangle=-45,
    height=600,
    paper_bgcolor='rgba(0,0,0,0)',  # Fondo externo transparente
    plot_bgcolor='rgba(0,0,0,0)',     # Fondo del área de gráfico transparente

)
fig_weapon_sev.update_xaxes(tickfont=dict(color='white'))
fig_weapon_sev.update_yaxes(tickfont=dict(color='white'))


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
    font=dict(color='white'),
    barmode='stack',
    xaxis_title='Ubication',
    yaxis_title='% of cases',
    template='plotly_white',
    xaxis_tickangle=-45,
    height=540,
    paper_bgcolor='rgba(0,0,0,0)',  # Fondo externo transparente
    plot_bgcolor='rgba(0,0,0,0)'    # Fondo del área de gráfico transparente

)
fig_loc_sev.update_xaxes(tickfont=dict(color='white'))
fig_loc_sev.update_yaxes(tickfont=dict(color='white'))



# Mostrar heatmap
st.plotly_chart(fig_heatmap, use_container_width=True)

st.header("Severity by weapon and location", divider ="orange")

# Mostrar gráficas apiladas
col3, col4 = st.columns(2)
with col3:
    st.subheader("Severity by weapon")
    st.plotly_chart(fig_weapon_sev, use_container_width=True)
    
    
with col4:
    st.subheader("Severity by location")
    st.plotly_chart(fig_loc_sev, use_container_width=True)


