from main import Chatbot
import streamlit as st

# Page configuration should be the first Streamlit command
st.set_page_config(page_title="AMC BOT")

# Sidebar configuration
with st.sidebar:
    st.title('Sanitation Bot')

# Caching the Chatbot instance to avoid reloading each time
@st.cache_resource
def get_chatbot():
    return Chatbot()

# Lazy-load the bot and create it only if it's called
def generate_response(input):
    bot = get_chatbot()
    return bot.rag_chain.invoke(input)

# Initialize session state for messages only once
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, ask me questions about AMC's Sanitation Services!"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Process user input and generate a response
if input_text := st.chat_input():
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.write(input_text)

    # Generate response only if the last message was from the user
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = generate_response(input_text)
                st.write(response)

            # Append assistant's response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})
