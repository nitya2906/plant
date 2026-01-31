import streamlit as st
import google.generativeai as genai   

# 🔑 Put your Gemini API key here
genai.configure(api_key="PASTE_YOUR_GEMINI_API_KEY_HERE")

model = genai.GenerativeModel("gemini-pro")

st.title("🌱 Plant Disease Chatbot (Gemini AI)")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Farmer Question:")

if st.button("Ask") and user_input:
    response = model.generate_content(user_input)
    st.session_state.chat.append(("Farmer", user_input))
    st.session_state.chat.append(("Bot", response.text))

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")

