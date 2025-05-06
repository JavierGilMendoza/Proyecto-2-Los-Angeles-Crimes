import streamlit as st
import base64


st.set_page_config(layout="wide")
# create_page = st.Page("streamlit_Aaron.py", title="Aaron")
# create_page2 = st.Page("streamlit.py", title="Ciara")
# create_page3 = st.Page("action_2_javi.py", title="Javi")


#poner fondo

def obtener_base64_local(imagen):
    with open(imagen, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

fondo_base64 = obtener_base64_local("fondopht.png")

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{fondo_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            color: white;  /* Cambiado a blanco */
        }}

        html, body, [class*="css"] {{
            background-color: transparent;
            color: white;  /* Cambiado a blanco */
        }}

        .stButton>button {{
            width: 100%;
            height: 50px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 12px;
            border: none;
            transition: 0.3s;
            background-color: #fff9c4;
            color: black;
        }}
        .stButton>button:hover {{
            transform: scale(1.05);
            background-color: #d0d0d0;
        }}

        .play-button button {{
            background-color: #4CAF50 !important;
            color: white;
        }}
        .reset-button button {{
            background-color: #f44336 !important;
            color: white;
        }}

        .choice-box {{
            text-align: center;
            padding: 15px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 10px;
            border: 2px solid #aaa;
            background-color: rgba(255,255,255,0.8);
            color: black;
        }}
    </style>
    """,
    unsafe_allow_html=True
)





pages = {
    "Menu": [
        st.Page("inicio.py", title="Inicio", icon="🔥"),
        st.Page("streamlit_Aaron.py", title="Aaron", icon="🔥"),
        st.Page("streamlit.py", title="Ciara",icon="🚨"),
        st.Page("action_2_javi.py", title="Javi",icon="🚨"),
        st.Page("streamlit_ale.py", title="Ale",icon="🚨"),
    ],
}


st.logo("logo.png")

pg = st.navigation(pages, expanded=True)
pg.run()