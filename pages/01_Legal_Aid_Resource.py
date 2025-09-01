import streamlit as st
from translator_config import SENTENCE

if 'lang' not in st.session_state:
    st.session_state.lang = "en"

st.title(SENTENCE["sent11"][st.session_state.lang])

states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

state_links = {
    "Alabama": "https://www.lawhelp.org/al",
    "Alaska": "https://www.lawhelp.org/ak",
    "Arizona": "https://www.lawhelp.org/az",
    "Arkansas": "https://www.lawhelp.org/ar",
    "California": "https://www.lawhelp.org/ca",
    "Colorado": "https://www.lawhelp.org/co",
    "Connecticut": "https://www.lawhelp.org/ct",
    "Delaware": "https://www.lawhelp.org/de",
    "Florida": "https://www.lawhelp.org/fl",
    "Georgia": "https://www.lawhelp.org/ga",
    "Hawaii": "https://www.lawhelp.org/hi",
    "Idaho": "https://www.lawhelp.org/id",
    "Illinois": "https://www.lawhelp.org/il",
    "Indiana": "https://www.lawhelp.org/in",
    "Iowa": "https://www.lawhelp.org/ia",
    "Kansas": "https://www.lawhelp.org/ks",
    "Kentucky": "https://www.lawhelp.org/ky",
    "Louisiana": "https://www.lawhelp.org/la",
    "Maine": "https://www.lawhelp.org/me",
    "Maryland": "https://www.lawhelp.org/md",
    "Massachusetts": "https://www.lawhelp.org/ma",
    "Michigan": "https://www.lawhelp.org/mi",
    "Minnesota": "https://www.lawhelp.org/mn",
    "Mississippi": "https://www.lawhelp.org/ms",
    "Missouri": "https://www.lawhelp.org/mo",
    "Montana": "https://www.lawhelp.org/mt",
    "Nebraska": "https://www.lawhelp.org/ne",
    "Nevada": "https://www.lawhelp.org/nv",
    "New Hampshire": "https://www.lawhelp.org/nh",
    "New Jersey": "https://www.lawhelp.org/nj",
    "New Mexico": "https://www.lawhelp.org/nm",
    "New York": "https://www.lawhelp.org/ny",
    "North Carolina": "https://www.lawhelp.org/nc",
    "North Dakota": "https://www.lawhelp.org/nd",
    "Ohio": "https://www.lawhelp.org/oh",
    "Oklahoma": "https://www.lawhelp.org/ok",
    "Oregon": "https://www.lawhelp.org/or",
    "Pennsylvania": "https://www.lawhelp.org/pa",
    "Rhode Island": "https://www.lawhelp.org/ri",
    "South Carolina": "https://www.lawhelp.org/sc",
    "South Dakota": "https://www.lawhelp.org/sd",
    "Tennessee": "https://www.lawhelp.org/tn",
    "Texas": "https://www.lawhelp.org/tx",
    "Utah": "https://www.lawhelp.org/ut",
    "Vermont": "https://www.lawhelp.org/vt",
    "Virginia": "https://www.lawhelp.org/va",
    "Washington": "https://www.lawhelp.org/wa",
    "West Virginia": "https://www.lawhelp.org/wv",
    "Wisconsin": "https://www.lawhelp.org/wi",
    "Wyoming": "https://www.lawhelp.org/wy"
}

selected_state = st.selectbox(SENTENCE["sent12"][st.session_state.lang], states)

if selected_state:
    st.markdown(f"[{SENTENCE['sent13'][st.session_state.lang]} {selected_state}]({state_links[selected_state]})", unsafe_allow_html=True)
