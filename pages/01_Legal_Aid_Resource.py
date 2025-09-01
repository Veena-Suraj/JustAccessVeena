import streamlit as st
from translator_config import SENTENCE
from rag import get_legal_aid_resources, translate_list

if 'lang' not in st.session_state:
    st.session_state.lang = "en"

with st.sidebar:
    option = st.selectbox(
            SENTENCE["sent6"][st.session_state.lang],
            ("English", "Spanish", "Hindi", "Vietnamese", "Mandarin"),
            placeholder=SENTENCE["sent7"][st.session_state.lang],
            index = None
        )
    # else select language
    if option == "English":
        st.session_state.lang = "en"
        st.rerun()
    elif option == "Spanish":
        st.session_state.lang = "sp"
        st.rerun()
    elif option == "Hindi":
        st.session_state.lang = "hi"
        st.rerun()
    elif option == "Vietnamese":
        st.session_state.lang = "vi"
        st.rerun()
    elif option == "Mandarin":
        st.session_state.lang = "zh"
        st.rerun()

st.title(SENTENCE["sent12"][st.session_state.lang])

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

translated_states = translate_list(states, st.session_state.lang)
state_map = dict(zip(translated_states, states))

selected_translated_state = st.selectbox(SENTENCE["sent13"][st.session_state.lang], translated_states)

if selected_translated_state:
    selected_english_state = state_map[selected_translated_state]
    with st.spinner('Finding resources...'):
        resources = get_legal_aid_resources(selected_english_state, st.session_state.lang)
        st.markdown(resources)
