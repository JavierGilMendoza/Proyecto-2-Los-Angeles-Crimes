import streamlit as st
import Basuras

# Menú lateral
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Elige una sección", [
    "Inicio",
    "Basura",
    "Pag vacia"
])

# Mostrar la sección correspondiente
if opcion == "Inicio":
    st.title("🔍 Análisis de Crímenes")
    st.write("Bienvenido. Selecciona una sección del menú lateral.")
elif opcion == "Basura":
    Basuras.mostrar()
