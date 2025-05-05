import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import plost

df = pd.read_csv('Data_Crime_Cleaning.csv')
descent_map = {
    'a': 'other asian',
    'b': 'black',
    'c': 'chinese',
    'd': 'cambodian',
    'f': 'filipino',
    'g': 'guamanian',
    'h': 'hispanic/latin/mexican',
    'i': 'american indian/alaskan native',
    'j': 'japanese',
    'k': 'korean',
    'l': 'laotian',
    'o': 'other',
    'p': 'pacific islander',
    's': 'samoan',
    'u': 'hawaiian',
    'v': 'vietnamese',
    'w': 'white',
    'x': 'unknown',
    'z': 'asian indian',
    '-': 'unknown',
}
df['descent_victim_map'] = df['descent_victim'].map(descent_map)
features_study = ['crime_severity','crime_code','crime_desc','crime_ucr','age_victim','sex_victim','descent_victim','crime_mo','descent_victim_map']
df_study = df[features_study]

#Plot Histogramas

# fig,axes = plt.subplots(nrows=2,ncols=2,figsize=(15,10))

# sns.histplot(df_study['crime_severity'],ax=axes[0,0])
# sns.histplot(df_study['sex_victim'],ax=axes[0,1])

# sns.histplot(df_study['crime_ucr'],ax=axes[1,0])
# axes[1, 0].tick_params(axis='x', rotation=90)
# sns.histplot(df_study['descent_victim_map'],ax=axes[1,1])
# axes[1, 1].tick_params(axis='x', rotation=90)

# plt.tight_layout()  #Asi ajusto el espacio entre los subplots
# plt.show()

st.title("Estudio de crimenes")

st.header("Histogramas")

chart_list = []
hist_list= ['crime_severity','sex_victim','crime_ucr','descent_victim_map']
for columna in hist_list:

    chart = {
        "mark": "bar",  # cambia el tipo de gráfico a barras
        "encoding": {
            "x": {
                "field": columna,
                "type": "nominal"  # categórico: USA, Europe, Japan
            },
            "y": {
                "aggregate": "count",  # contar cuántos por categoría
                "type": "quantitative"
            },
            "color": {
                "field": columna,
                "type": "nominal"
            }
        }
    }
    chart_list.append(chart)

tab1, tab2, tab3, tab4 = st.tabs(["Histograma crime_severity", "Histograma de sex_victim", "Histograma de crime_ucr", "Histograma de descent_victim_map"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.vega_lite_chart(
        df_study, chart_list[0], theme=None, use_container_width=True
    )
with tab2:
    st.vega_lite_chart(
        df_study, chart_list[1], theme=None, use_container_width=True
    )
with tab3:
    st.vega_lite_chart(
        df_study, chart_list[2], theme=None, use_container_width=True
    )
with tab4:
    st.vega_lite_chart(
        df_study, chart_list[3], theme=None, use_container_width=True
    )


container_1 = st.container(border=True)

container_1.col1, container_1.col2 = st.columns(2)


with container_1.col1:
    df_study_severity = df_study.groupby('crime_severity').size().reset_index(name='count')
    st.bar_chart(df_study_severity, x="crime_severity", y="count", color="crime_severity", horizontal =False )


with container_1.col2:
    df_study_sex = df_study.groupby('sex_victim').size().reset_index(name='count')
    st.bar_chart(df_study_sex, x="sex_victim", y="count", color="sex_victim", horizontal = False)

container_2 = st.container(border=True)
container_2.col1, container_2.col2 = st.columns(2)

with container_2.col1:
    df_study_severity = df_study.groupby('crime_ucr').size().reset_index(name='count')
    st.bar_chart(df_study_severity, x="crime_ucr", y="count", color="crime_ucr", horizontal = False, x_label ="")

with container_2.col2:
    df_study_severity = df_study.groupby('descent_victim_map').size().reset_index(name='count')
    st.bar_chart(df_study_severity, x="descent_victim_map", y="count", color="descent_victim_map", horizontal = False)


st.divider()
st.subheader("Boxplot")

chart = alt.Chart(df_study).mark_boxplot(size=15, outliers=False).encode(
    y=alt.Y('crime_ucr:N', title='Crimenes'),         
    x=alt.X('age_victim:Q', title='Edad de la victima'),   
    color='crime_ucr:N'
).properties(width='container', height=300)
st.altair_chart(chart, use_container_width=True)


with st.container():
    st.markdown("""
        <style>
        .block-container > div {
            background-color: #f9f9f9;
            border: 2px solid green;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("Heatmap")

df_study_without_unknown = df_study.loc[df_study['descent_victim_map'] != 'unknown']
heatmap_data = pd.crosstab(df_study_without_unknown['descent_victim_map'], df_study_without_unknown['crime_ucr'])


# Crear el heatmap
fig, ax = plt.subplots()
sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')

st.pyplot(fig)