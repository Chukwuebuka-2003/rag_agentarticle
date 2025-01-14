import streamlit as st
import os
from main import ArticleCrew

# Load API keys from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# App title
st.title("PDF to Article Generator")

# Initialize session state for conversations
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

# Load previous conversation if selected
def load_conversation(conversation_id):
    st.session_state.current_conversation = st.session_state.conversations[conversation_id]

# Sidebar for managing conversations
st.sidebar.title("Previous Conversations")
if st.session_state.conversations:
    conversation_ids = list(st.session_state.conversations.keys())
    selected_conversation = st.sidebar.selectbox("Select a conversation:", conversation_ids)
    if st.sidebar.button("Load Conversation"):
        load_conversation(selected_conversation)

# File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    # Save uploaded file temporarily
    temp_path = f"/tmp/{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"PDF uploaded and ready to process: {uploaded_file.name}")

    # User input for search query
    user_input = st.text_input("Enter your search query:")
    if user_input:
        # Initialize ArticleCrew with inputs and file path
        inputs = {"user_input": user_input, "file_path": temp_path}
        article_crew = ArticleCrew(inputs=inputs)

        try:
            # Execute the CrewAI workflow
            response = article_crew.run()
            st.write("### Final Output:")
            st.markdown(response)  # Display the output

            # Store the current conversation in session state
            if "current_conversation" not in st.session_state:
                st.session_state.current_conversation = []

            st.session_state.current_conversation.append({"role": "user", "content": user_input})
            st.session_state.current_conversation.append({"role": "assistant", "content": response})

            # Save conversation with a unique ID
            import uuid
            conversation_id = str(uuid.uuid4())
            st.session_state.conversations[conversation_id] = st.session_state.current_conversation

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a PDF to begin.")
