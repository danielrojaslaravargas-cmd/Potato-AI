import streamlit as st
import google.generativeai as genai

try:
    API_KEY = st.secrets[AIzaSyCRZX0ZEY5ebsMCSxviyLiFQunwN0_HO7c]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(AIzaSyCRZX0ZEY5ebsMCSxviyLiFQunwN0_HO7c)
    st.stop()

st.set_page_config(page_title="POTATO AI 🥔", page_icon="🥔")

st.markdown("""
    <style>
    .stApp { background-color: #050805; color: #f0fff0; }
    .stChatMessage { 
        border-radius: 25px; 
        border: 2px solid #2e7d32; 
        background-color: #141d14 !important;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("POTATO AI 🥔")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something earthy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="You are Potato AI, a punny potato assistant."
        )
        response = model.generate_content(prompt)
        ai_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
    except Exception as e:
        st.error(f"Soil Error: {e}")
