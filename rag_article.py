import streamlit as st
from main import ArticleCrew
import os
import uuid

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]


if "conversations" not in st.session_state:
    st.session_state.conversations = {}

def load_conversation(conversation_id):
    st.session_state.current_conversation = st.session_state.conversations[conversation_id]


st.sidebar.title("Previous Conversations")

if st.session_state.conversations:
    conversation_ids = list(st.session_state.conversations.keys())
    selected_conversation = st.sidebar.selectbox("Select a conversation:", conversation_ids)
    if st.sidebar.button("Load Conversation"):
        load_conversation(selected_conversation)
    else:
        st.sidebar.write("No previous conversations")


st.title("Create Articles Powered by RAG")
st.write("RAG is an interesting concept, but now think about creating articles based on the contents of the RAG which is powered by AI Agents")

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = []

for message in st.session_state.current_conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your question"):

    st.session_state.current_conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    inputs = "\n".join([msg["content"] for msg in st.session_state.current_conversation if msg["role"] == "user"])
    research_crew = ArticleCrew(inputs)

    response = research_crew.run()


    st.session_state.current_conversation.append({"role":"assistant","content":response})
    with st.chat_message("assistant"):
        st.markdown(response)


    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = st.session_state.current_conversation