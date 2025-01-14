import streamlit as st
from main import ArticleCrew
import os
import uuid

# API keys from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# Initialize session state for conversations
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = []

# Function to load a previous conversation
def load_conversation(conversation_id):
    st.session_state.current_conversation = st.session_state.conversations[conversation_id]

# Sidebar for previous conversations
st.sidebar.title("Previous Conversations")

if st.session_state.conversations:
    conversation_ids = list(st.session_state.conversations.keys())
    selected_conversation = st.sidebar.selectbox("Select a conversation:", conversation_ids)
    if st.sidebar.button("Load Conversation"):
        load_conversation(selected_conversation)
else:
    st.sidebar.write("No previous conversations")

# Main application title and description
st.title("Create Articles Powered by RAG")
st.write("RAG is an interesting concept, but now think about creating articles based on the contents of the RAG, which is powered by AI Agents.")

# PDF Upload Section
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded PDF temporarily
    temp_file_path = f"temp_{uuid.uuid4()}.pdf"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display a success message
    st.success(f"Uploaded PDF: {uploaded_file.name}")

    # Process the PDF file with ArticleCrew
    st.write("Processing the PDF file...")
    research_crew = ArticleCrew(inputs=temp_file_path)

    # Run the ArticleCrew with the PDF content
    response = research_crew.run()

    # Show the response
    st.session_state.current_conversation.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Display conversation history
for message in st.session_state.current_conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input in the chat
if prompt := st.chat_input("Enter your question"):
    st.session_state.current_conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Combine inputs and run RAG
    inputs = "\n".join([msg["content"] for msg in st.session_state.current_conversation if msg["role"] == "user"])
    research_crew = ArticleCrew(inputs)
    response = research_crew.run()

    # Display and save the assistant's response
    st.session_state.current_conversation.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save the conversation
    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = st.session_state.current_conversation