import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.title("Groq LLM Chatbot")

if not api_key:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=api_key
)

user_input = st.text_input("Enter your prompt:")

if st.button("Ask"):
    with st.spinner("Thinking..."):
        response = llm.invoke([HumanMessage(content=user_input)])
    st.write(response.content)
