import streamlit as st
import requests
import random

# Configuración de la página
st.set_page_config(
    page_title="🎵 YouTube Music Explorer",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
        .main {
            background-color: #121212;
            color: #ffffff;
        }
        .stSelectbox label, .stButton button {
            color: #1DB954 !important;
        }
        h1 {
            color: #1DB954 !important;
        }
        .stVideo {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Título
st.title("🎵 YouTube Music Explorer")

# Selector de género con íconos
genre = st.selectbox(
    "Selecciona un género musical:",
    ["pop", "rock", "jazz", "electrónica", "latina", "relajante"],
    format_func=lambda x: {
        "pop": "Pop 🎤",
        "rock": "Rock 🎸",
        "jazz": "Jazz 🎷",
        "electrónica": "Electrónica 🎛️",
        "latina": "Latina 🥥",
        "relajante": "Relajante 🧘‍♂️"
    }[x]
)

if st.button("🎵 ¡Reproducir canción aleatoria!"):
    # API Key de YouTube (debes crearla en Google Cloud Console)
    API_KEY = "AIzaSyDF2HqnhLnth_FhQ-zEw-6Hh75H-PV3BgY"
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": f"{genre} music official video",
        "type": "video",
        "maxResults": 10,
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        video = random.choice(data["items"])
        video_id = video["id"]["videoId"]
        video_title = video["snippet"]["title"]
        video_channel = video["snippet"]["channelTitle"]

        st.subheader(f"**{video_title}**")
        st.write(f"por {video_channel}")
        st.video(f"https://www.youtube.com/embed/{video_id}")
    else:
        st.error("No se encontraron videos. Intenta con otro género.")