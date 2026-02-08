import streamlit as st
import google.generativeai as genai

# --- 1. SETTINGS & BRAIN ---
# Check for the API Key in Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Use the key provided if secrets aren't set
    API_KEY = "AIzaSyAR3wLcR4yLwHXLmJAavohHjaE3O5gVDUg"

# Configure the library
genai.configure(api_key=API_KEY)

# --- 2. BUBBLY GREEN UI ---
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
    .stProgress > div > div > div > div { background-color: #81c784; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MEMORY SYSTEM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. THE INTERFACE ---
st.title("POTATO AI 🥔")

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Ask your spud..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # We call the model directly here - this avoids the 404 error!
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Get response
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Show AI response
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        # Save to memory
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
    except Exception as e:
        # If it still fails, it will show the specific reason
        st.error(f"Soil Error: {e}")
