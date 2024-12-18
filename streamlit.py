from main import Chatbot
import streamlit as st
import re

# Page configuration
st.set_page_config(page_title="Sanitation BOT")

# Sidebar configuration
with st.sidebar:
    st.title("Chatbot for the Ahmedabad Municipal Corporation Sanitation Services")

# Cache the Chatbot instance
@st.cache_resource
def get_chatbot():
    return Chatbot()

# Lazy-load the bot and create it only if called
def generate_response(input_text):
    bot = get_chatbot()
    return bot.rag_chain.invoke(input_text)

# Initialize session state for messages only once
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Ask me questions about the Sanitation Policies of AMC."}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Process user input and generate response
if input_text := st.chat_input():
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.write(input_text)

    # Generate response only if the last message was from the user
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = generate_response(input_text)

            # Format long responses as bullet points, removing any pre-existing numbers
            if isinstance(response, str) and len(response) > 100:
                # Remove any numbers at the start of each sentence (e.g., "1 ", "2 ")
                response_parts = re.sub(r"^\d+\s+", "", response, flags=re.MULTILINE).split(". ")
                formatted_response = "\n".join(f"- {part.strip()}" for part in response_parts if part.strip())
                st.markdown(formatted_response)
            else:
                st.write(response)

        # Append assistant's response to session state
        st.session_state.messages.append({"role": "assistant", "content": formatted_response})


