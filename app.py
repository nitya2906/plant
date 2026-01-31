import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-pro")  # or use gemini-1.5

st.title("🌿 Plant Disease Chatbot (Powered by Gemini AI)")
st.write("Ask anything about plant diseases, symptoms, and treatments.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input
user_message = st.text_input("You:")

if st.button("Send") and user_message:
    # Add to history
    st.session_state.chat_history.append(("User", user_message))
    
    # Send to Gemini
    chat = model.start_chat(history=[])
    response_chunks = chat.send_message(user_message, stream=True)

    bot_reply = ""
    for chunk in response_chunks:
        bot_reply += chunk.text

    # Save bot reply
    st.session_state.chat_history.append(("Bot", bot_reply))

# Display conversation
for sender, text in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {text}")
