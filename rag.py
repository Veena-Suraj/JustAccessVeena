import os
import base64
import requests

import streamlit as st
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pinecone import Pinecone


# keys
os.environ["OPENAI_API_KEY"] = st.secrets["llm"]["OPENAI_API_KEY"]
os.environ["PINECONE_API_KEY"] = st.secrets["llm"]["PINECONE_API_KEY"]
os.environ["INDEX_HOST"] = st.secrets["llm"]["INDEX_HOST"]

# constants
NAMESPACE_KEY = "JAV"
TEXT_MODEL = "text-embedding-ada-002"
QA_MODEL = "gpt-4o-mini"
COMMON_ENGLISH_TEMPLATE = """
"You are a highly trained Legal Aid Navigator."
"Use the following pieces of context to answer the question at the end with human readable answer as a paragraph"
"Please do not use data outside the context to answer any questions. "
"If the answer is not in the given context, just say that you don't have enough context."
"don't try to make up an answer. "
"\n\n"
{context}
"\n\n"
Question: {question}
"n"
"Helpful answer:   "
"""

ENGLISH_TO_SPANISH_TEMPLATE = """
"You are highly trained language translation assistant."
"Use the following piece of context in english and translate it to spanish"
"Please do not use data outside the context to translate any questions."
"don't try to make up a translation."
"\n\n"
{context}
"\n\n"
Translation:
"""
ENGLISH_TO_HINDI_TEMPLATE = """
"You are highly trained language translation assistant."
"Use the following piece of context in english and translate it to hindi"
"Please do not use data outside the context to translate any questions."
"don't try to make up a translation."
"\n\n"
{context}
"\n\n"
Translation:
"""

SPANISH_TO_ENGLISH_TEMPLATE = """
"You are highly trained language translation assistant."
"Use the following piece of context in spanish and translate it to english"
"Please do not use data outside the context to translate any questions."
"don't try to make up an translation."
"\n\n"
{context}
"\n\n"
Translation:
"""
HINDI_TO_ENGLISH_TEMPLATE = """
"You are highly trained language translation assistant."
"Use the following piece of context in hindi and translate it to english"
"Please do not use data outside the context to translate any questions."
"don't try to make up a translation."
"\n\n"
{context}
"\n\n"
Translation:
"""

# pinecone setup
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host=os.environ["INDEX_HOST"])

# create client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_openai_embeddings(text: str) -> list[float]:
    response = client.embeddings.create(input=f"{text}", model=TEXT_MODEL)

    return response.data[0].embedding


# function query similar chunks
def query_response(query_embedding, k = 1, namespace_ = NAMESPACE_KEY):
    query_response = index.query(
        namespace=namespace_,
        vector=query_embedding,
        top_k=k,
        include_values=False,
        include_metadata=True,
    )

    return query_response


def content_extractor(similar_data):
    top_values = similar_data["matches"]
    # get the text out
    text_content = [sub_content["metadata"]["text"] for sub_content in top_values]
    return " ".join(text_content)


def get_model():
    model = ChatOpenAI(model=QA_MODEL, api_key=os.environ["OPENAI_API_KEY"])
    return model


def translator(context: str, lang: str):
    if lang == "en":
        template = SPANISH_TO_ENGLISH_TEMPLATE
    else:
        if lang == "sp":
            template = ENGLISH_TO_SPANISH_TEMPLATE
        elif lang == "hi":
            template = HINDI_TO_ENGLISH_TEMPLATE
    prompt = ChatPromptTemplate.from_template(template)
    model = get_model()
    output_parser = StrOutputParser()

    # create the chain
    chain = prompt | model | output_parser

    # get the answer
    translation = chain.invoke({"context": context})

    return translation


def get_similar_context(question: str, lang: str):
    if lang == "sp":
        question = str(translator(question, "en"))
    elif lang == "hi":
        question = str(translator(question, "en"))
    # get the query embeddings
    quer_embed_data = get_openai_embeddings(question)

    # query the similar chunks
    similar_chunks = query_response(quer_embed_data)

    # extract the similar text data
    similar_content = content_extractor(similar_chunks)

    return similar_content, question


def streaming_question_answering(query_question: str, context_text: str, lang: str, template: str = COMMON_ENGLISH_TEMPLATE):
    prompt = ChatPromptTemplate.from_template(template)
    model = get_model()
    output_parser = StrOutputParser()

    if lang == "en":
        # create the chain
        chain = prompt | model | output_parser

        # get the answer
        return chain.stream({"context": context_text, "question": query_question})
    elif lang == "sp":
        translate_prompt = ChatPromptTemplate.from_template(ENGLISH_TO_SPANISH_TEMPLATE)
        # create the chain
        chain = prompt | model | output_parser

        answer = chain.invoke({"context": context_text, "question": query_question})

        language_chain = translate_prompt | model | output_parser

        return language_chain.stream({"context": answer})
    elif lang == "hi":
        translate_prompt = ChatPromptTemplate.from_template(HINDI_TO_ENGLISH_TEMPLATE)
        # create the chain
        chain = prompt | model | output_parser

        answer = chain.invoke({"context": context_text, "question": query_question})

        language_chain = translate_prompt | model | output_parser

        return language_chain.stream({"context": answer})
        
