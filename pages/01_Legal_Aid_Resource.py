import streamlit as st
from translator_config import SENTENCE
from rag import get_legal_aid_resources

if 'lang' not in st.session_state:
    st.session_state.lang = "en"

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

selected_state = st.selectbox(SENTENCE["sent13"][st.session_state.lang], states)

if selected_state:
    with st.spinner('Finding resources...'):
        resources = get_legal_aid_resources(selected_state)
        st.markdown(resources)
