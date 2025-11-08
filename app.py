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
    API_KEY = os.getenv("YOUTUBE_API_KEY")
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
            for item in st.session_state.history:
                st.sidebar.write(f"• {item['title']} - {item['channel']} ({item['timestamp']})")
    else:
        st.error("No videos found. Try another genre.")