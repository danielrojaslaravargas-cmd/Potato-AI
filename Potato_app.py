import streamlit as st
import google.generativeai as genai

try:
    API_KEY = st.secrets["gemini_key"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Check Secrets!")
    st.stop()

st.set_page_config(page_title="POTATO AI 🥔")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("POTATO AI 🥔")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your spud..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Changed 'gemini-1.5-flash' to 'models/gemini-1.5-flash'
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash',
            system_instruction="You are Potato AI, a punny potato assistant."
        )
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Soil Error: {e}")
