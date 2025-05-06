import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import plost
import base64



def obtener_base64_local(imagen):
    with open(imagen, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

fondo_base64 = obtener_base64_local("fondo_app.png")

df = pd.read_csv('Data_Crime_Cleaning.csv')
descent_map = {
    'a': 'other asian',
    'b': 'black',
    'c': 'chinese',
    'd': 'cambodian',
    'f': 'filipino',
    'g': 'guamanian',
    'h': 'latin',
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

st.title("Crime study")
st.divider()


st.header("Count of crime agrouping and descent victim", divider="orange")

# chart_list = []
# hist_list= ['crime_severity','sex_victim','crime_ucr','descent_victim_map']
# for columna in hist_list:

#     chart = {
#         "mark": "bar",  # cambia el tipo de gráfico a barras
#         "encoding": {
#             "x": {
#                 "field": columna,
#                 "type": "nominal"  # categórico: USA, Europe, Japan
#             },
#             "y": {
#                 "aggregate": "count",  # contar cuántos por categoría
#                 "type": "quantitative"
#             },
#             "color": {
#                 "field": columna,
#                 "type": "nominal"
#             }
#         }
#     }
#     chart_list.append(chart)

# tab1, tab2, tab3, tab4 = st.tabs(["Histograma crime_severity", "Histograma de sex_victim", "Histograma de crime_ucr", "Histograma de descent_victim_map"])


# with tab1:
#     # Use the Streamlit theme.
#     # This is the default. So you can also omit the theme argument.
#     st.vega_lite_chart(
#         df_study, chart_list[0], theme=None, use_container_width=True
#     )
# with tab2:
#     st.vega_lite_chart(
#         df_study, chart_list[1], theme=None, use_container_width=True
#     )
# with tab3:
#     st.vega_lite_chart(
#         df_study, chart_list[2], theme=None, use_container_width=True
#     )
# with tab4:
#     st.vega_lite_chart(
#         df_study, chart_list[3], theme=None, use_container_width=True
#     )


# container_1 = st.container(border=True)


# container_1.col1, container_1.col2 = st.columns(2)


# with container_1.col1:
#     df_study_severity = df_study.groupby('crime_severity').size().reset_index(name='count')
#     st.bar_chart(df_study_severity, x="crime_severity", y="count", color="crime_severity", horizontal =False )


# with container_1.col2:
#     df_study_sex = df_study.groupby('sex_victim').size().reset_index(name='count')
#     st.bar_chart(df_study_sex, x="sex_victim", y="count", color="sex_victim", horizontal = False)

container_2 = st.container(border=True)
container_2.col1, container_2.col2 = st.columns(2)


with container_2.col1:
    df_study_severity = df_study.groupby('crime_ucr').size().reset_index(name='count')
    st.subheader("Count of crime group")
    # Ordenar por 'count' de mayor a menor
    chart1 = alt.Chart(df_study_severity).mark_bar().encode(
        x=alt.X('crime_ucr:N', title='', sort=alt.EncodingSortField(field="count", op="sum", order="descending")),  # Ordenar
        y='count:Q',
        color='crime_ucr:N'
    ).properties(
        height=400,
        background='rgba(0,0,0,0)'  # Fondo transparente
    ).configure_axis(
    labelColor='white',
    titleColor='white'
)
    
    st.altair_chart(chart1, use_container_width=True)

with container_2.col2:
    df_study_severity = df_study.groupby('descent_victim_map').size().reset_index(name='count')
    df_study_severity = df_study_severity.loc[df_study_severity['descent_victim_map'] != 'unknown']
    st.subheader("Count of descent victim")

    chart2 = alt.Chart(df_study_severity).mark_bar().encode(
        x=alt.X('descent_victim_map:N', title='',sort=alt.EncodingSortField(field="count", op="sum", order="descending")),
        y='count:Q',
        color='descent_victim_map:N'
    ).properties(
        height=400,
        background='rgba(0,0,0,0)'  #  Fondo transparente
    ).configure_axis(
    labelColor='white',
    titleColor='white'
)
    st.altair_chart(chart2, use_container_width=True)

#----------------------------------------------------------------------------------
st.divider()
st.header("Descent victim by crime group", divider="orange")
top_4_descent = df_study['descent_victim_map'].value_counts().nlargest(4).index
df_filtro_descent = df_study[df_study['descent_victim_map'].isin(top_4_descent)]

top_5_crime_ucr = df_filtro_descent['crime_ucr'].value_counts().nlargest(5).index
df_filtro_crime = df_filtro_descent[df_filtro_descent['crime_ucr'].isin(top_5_crime_ucr)]
count_df = df_filtro_crime.groupby(['crime_ucr', 'descent_victim_map']).size().reset_index(name='count')
count_df = count_df.loc[count_df['descent_victim_map']!= 'unknown']
# plt.figure(figsize=(12, 6))
# sns.barplot(data=count_df, x='crime_ucr', y='conteo', hue='descent_victim_map')
# plt.title('Conteo de cada crimen por descent_victim_map')
# plt.tight_layout()
# plt.show()


df_study_severity = df_study.groupby('crime_ucr').size().reset_index(name='count')
    
    # Ordenar por 'count' de mayor a menor
chart4 = alt.Chart(count_df).mark_bar().encode(
    x=alt.X('crime_ucr:N', title='', sort=alt.EncodingSortField(field="count", op="sum", order="descending")),
    xOffset='descent_victim_map:N',  # Agrupar barras por origen étnico
    y=alt.Y('count:Q', title='count'),
    color=alt.Color('descent_victim_map:N', title='Origen'),
    tooltip=['crime_ucr:N', 'descent_victim_map:N', 'count:Q']
).properties(
    height=400,
    background='rgba(0,0,0,0)'
).configure_axis(
    labelColor='white',
    titleColor='white',
    labelAngle=0
)


st.altair_chart(chart4, use_container_width=True)


plt.figure(figsize=(12, 6))
sns.barplot(data=count_df, x='crime_ucr', y='count', hue='descent_victim_map')
plt.title('Crimen group count per descent victim')
plt.tight_layout()
plt.show()

#--------------------------------------------------------------------------------------------

st.divider()
st.header("Boxplot of age victim by crime group", divider="orange")

chart = alt.Chart(df_study).mark_boxplot(size=25, outliers=False).encode(
    y=alt.Y('crime_ucr:N', title='Crime group'),         
    x=alt.X('age_victim:Q', title='Age victim'),   
    color='crime_ucr:N'
).properties(width='container', height=600, background='rgba(0,0,0,0)').configure_axis(
    labelColor='white',
    titleColor='white'
)
st.altair_chart(chart, use_container_width=True)





# df_study_without_unknown = df_study.loc[df_study['descent_victim_map'] != 'unknown']
# heatmap_data = pd.crosstab(df_study_without_unknown['descent_victim_map'], df_study_without_unknown['crime_ucr'])


# # Crear el heatmap
# fig, ax = plt.subplots()
# sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')

# st.pyplot(fig)
