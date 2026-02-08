import streamlit as st
import google.generativeai as genai

API_KEY = "AIzaSyAR3wLcR4yLwHXLmJAavohHjaE3O5gVDUg"

genai.configure(api_key=API_KEY, transport='rest') 

st.set_page_config(page_title="POTATO AI 🥔", page_icon="🥔")
st.markdown("""
    <style>
    .stApp { background-color: #050805; color: #f0fff0; }
    .stChatMessage { border-radius: 25px; border: 2px solid #2e7d32; background-color: #141d14 !important; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("POTATO AI 🥔")

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your spud..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # This will now give us a very detailed error if it fails
        st.error(f"Soil Error: {e}")
