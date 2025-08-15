from openai import OpenAI
import streamlit as st

from translator_config import SENTENCE
from rag import QA_MODEL, streaming_question_answering, get_similar_context


if not st.experimental_user.is_logged_in:
    st.error(SENTENCE["sent9"][st.session_state.lang])
    st.stop()

if 'lang' not in st.session_state:
    st.session_state.lang = "en"

with st.sidebar:
    option = st.selectbox(
            SENTENCE["sent6"][st.session_state.lang],
            ("English", "Spanish", "Hindi"),
            placeholder=SENTENCE["sent7"][st.session_state.lang],
            index = None
        )
    # else select language
    if option == "English":
        st.session_state.lang = "en"
        st.session_state.messages = []
        st.rerun()
    elif option == "Spanish":
        st.session_state.lang = "sp"
        st.session_state.messages = []
        st.rerun()
    elif option == "Hindi":
        st.session_state.lang = "hi"
        st.session_state.messages = []
        st.rerun()

# chatbot
FIRST_MESSAGE = {"role": "assistant", "content": SENTENCE["sent8"][st.session_state.lang]}

# set the title
st.title(SENTENCE["sent10"][st.session_state.lang])

if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [FIRST_MESSAGE]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        print("=====",message["content"])
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        pinecone_context, question = get_similar_context(prompt, st.session_state.lang)
        response = st.write_stream(streaming_question_answering(question, pinecone_context, st.session_state.lang))
    st.session_state.messages.append({"role": "assistant", "content": response})
