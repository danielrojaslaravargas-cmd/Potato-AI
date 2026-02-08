import streamlit as st
from google import genai

# --- 1. SETTINGS & BRAIN ---
# This part looks for your API Key in Streamlit's "Secrets"
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # If secrets aren't set yet, it uses your provided key
    API_KEY = "AIzaSyAR3wLcR4yLwHXLmJAavohHjaE3O5gVDUg"

client = genai.Client(api_key=API_KEY)

# This tells the AI exactly how to behave
SYSTEM_INSTRUCTION = (
    "You are Potato AI. You are a helpful, friendly, and punny potato assistant. "
    "You remember everything the user tells you in this chat. "
    "Use potato-themed humor (spud-tacular, starch, eyes, peeling great)."
)

# --- 2. BUBBLY GREEN UI ---
st.set_page_config(page_title="POTATO AI 🥔", page_icon="🥔")

st.markdown("""
    <style>
    /* Background and text colors */
    .stApp { background-color: #050805; color: #f0fff0; }
    
    /* Customizing the chat bubbles */
    .stChatMessage { 
        border-radius: 25px; 
        border: 2px solid #2e7d32; 
        background-color: #141d14 !important;
        margin-bottom: 10px;
    }
    
    /* Making the progress bar green */
    .stProgress > div > div > div > div { background-color: #81c784; }
    
    /* Styling the input box */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MEMORY SYSTEM ---
# This keeps the conversation going even when the page refreshes
if "messages" not in st.session_state:
    st.session_state.messages = []

if "soil_level" not in st.session_state:
    st.session_state.soil_level = 0

# --- 4. THE INTERFACE ---
st.title("POTATO AI 🥔")
st.write(f"Soil Nutrition (Level {st.session_state.soil_level // 100 + 1})")
st.progress(min((st.session_state.soil_level % 100) / 100, 1.0))

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Ask your spud..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate response using the full history for memory
        # We format the history to match what the Google SDK expects
        history_for_api = []
        for m in st.session_state.messages:
            history_for_api.append({"role": m["role"], "parts": [{"text": m["content"]}]})

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config={"system_instruction": SYSTEM_INSTRUCTION},
            contents=history_for_api
        )
        
        ai_response = response.text
        
        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        # Save to memory
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Increase Soil Level
        st.session_state.soil_level += 20
        if st.session_state.soil_level % 100 == 0:
            st.balloons()

    except Exception as e:
        st.error(f"Soil Error: {e}")

# --- 6. SIDEBAR TOOLS ---
with st.sidebar:
    st.header("Potato Shed")
    if st.button("Clear Memory 🗑️"):
        st.session_state.messages = []
        st.session_state.soil_level = 0
        st.rerun()
