import streamlit as st
import requests
import random
import os
import datetime

st.set_page_config(
    page_title="🎵 YouTube Music Explorer",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
        section[data-testid="stSidebar"] {
            width: 300px !important;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 YouTube Music Explorer")

genre = st.selectbox(
    "Select a music genre:",
    [
        "pop", "rock", "jazz", "electronic", "latin", "relaxing",
        "hip hop", "classical", "country", "reggaeton", "indie",
        "metal", "blues", "soul", "disco", "punk"
    ],
    format_func=lambda x: {
        "pop": "Pop 🎤",
        "rock": "Rock 🎸",
        "jazz": "Jazz 🎷",
        "electronic": "Electronic 🎛️",
        "latin": "Latin 🥥",
        "relaxing": "Relaxing 🧘‍♂️",
        "hip hop": "Hip Hop 🎤",
        "classical": "Classical 🎼",
        "country": "Country 🤠",
        "reggaeton": "Reggaeton 🥥",
        "indie": "Indie 🎸",
        "metal": "Metal 🤘",
        "blues": "Blues 🎷",
        "soul": "Soul 🎹",
        "disco": "Disco 🕺",
        "punk": "Punk 🤪"
    }[x]
)

if st.button("🎵 Play random song!"):
    st.session_state.selected_genre = genre
    if ("current_results" not in st.session_state or
    st.session_state.last_genre != genre ):
        API_KEY = os.getenv("YOUTUBE_API_KEY")

        if not API_KEY:
            st.error("⚠️ API Key missing. Contact the developer.")
            st.stop()

    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": f"{genre} music official video",
        "type": "video",
        "maxResults": 50,
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        st.session_state.current_results = data["items"]
        st.session_state.last_genre = genre
        st.session_state.current_index = 0  
        st.session_state.played_indices = set()  
        available_indices = [
        i for i in range(len(data["items"]))
        if i not in st.session_state.played_indices ]

        if available_indices:
            # Elegir un índice aleatorio entre los disponibles
            index = random.choice(available_indices)
            st.session_state.current_index = index
            st.session_state.played_indices.add(index)
    else:
        st.error("No videos found. Try another genre.")
        st.session_state.current_results = []

if "current_results" in st.session_state and st.session_state.current_results:
    results = st.session_state.current_results
    video = results[index]
    video_id = video["id"]["videoId"]
    video_title = video["snippet"]["title"]
    video_channel = video["snippet"]["channelTitle"]

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "title": video_title,
        "channel": video_channel,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    })

    st.subheader(f"**{video_title}**")
    st.write(f"by {video_channel}")

    st.video(f"https://www.youtube.com/embed/{video_id}")

    st.sidebar.subheader("🎵 Recently Played")
    for item in reversed(st.session_state.history):
        st.sidebar.write(f"• {item['title']} - {item['channel']} ({item['timestamp']})")

    
    available_indices = [i for i in range(len(results)) if i not in st.session_state.played_indices]
    if available_indices:
        if st.button("⏭️ Next song", key="next_song_button"):
            next_index = random.choice(available_indices)
            st.session_state.current_index = next_index
            st.session_state.played_indices.add(next_index)
            st.rerun()
    else:
        st.info("No more songs available for this genre. Try another one!")
else:
    st.info("No more songs available for this genre. Try another one!")


