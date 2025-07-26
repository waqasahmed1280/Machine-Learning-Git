import streamlit as st
from google import generativeai as genai
from google.generativeai.types import GenerationConfig
import os
from dotenv import load_dotenv
import random
import re
# --- Page and Model Configuration ---

st.set_page_config(
    page_title="Chat with Rudy 😼",
    page_icon="😼",
    layout="centered",
    initial_sidebar_state="collapsed" # Start with the sidebar collapsed
)

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- Asset Definitions ---

RUDE_CAT_GIFS = [
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExazd2ZWd5cGdtMGMwa3Jod2xseGxreTE4czRxMG00ZGF1MnlyZWp2NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YmVNzDnboB0RQEpmLr/giphy.gif",
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2M3dGNxOWY1bmN4MXcyd2M4c29uYThncjc3aWE2eGd5ZzI3OTluZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7rBemb9RiAEtW/giphy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2FxZTg5NzAxa2FjYXNnZ3JhYnN5a3c0M2ZibGp5c3d1N3M1ZmN3NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bcqAMUTUHoLDy/giphy.gif",
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3Bxdnl6cjAxcGtuZ3RkMTExNGN1dDhucjc3ZG52c3hxOHUxbmZsdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HtYsYjPsw1nVu/giphy.gif",
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXlldTE0M2RiNzJwaTV0ZnNjODkzdTE5eWd6dXFsMDk4emg4am82YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hRPoV9O14t3vW/giphy.gif",
]

# --- CSS for Modern UI ---

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        /* --- Global Styles --- */
        /* Apply Poppins to all text, but not icons */
        html, body, .st-emotion-cache-1gulkj5, .st-emotion-cache-1yyy949, .st-emotion-cache-l99sz9, .st-emotion-cache-ue6h4q, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1xsh3k6, .st-emotion-cache-1c7y2kd {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Hide default Streamlit header/footer */
        .st-emotion-cache-16txtl3, .st-emotion-cache-12fmjuu { 
            display: none;
        }
        
        .stApp { /* Main app container */
            background-color: #0d1117; /* GitHub Dark Background */
            color: #c9d1d9; /* GitHub Dark Text */
            padding-bottom: 120px; /* Space for the fixed input bar */
        }

        /* --- Main Title Style --- */
        .main-title {
            font-size: 2.5rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 1.5rem;
            background: -webkit-linear-gradient(45deg, #8a2be2, #c9d1d9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* --- Sidebar Styles --- */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        [data-testid="stSidebar"] .stButton button {
            background-color: #30363d;
            color: #c9d1d9;
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background-color: #8a2be2;
            color: #fff;
            border: 1px solid #8a2be2;
        }

        /* --- Chat Message Styling --- */
        .chat-message {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1.5rem;
            width: 100%;
        }
        .chat-message.user { justify-content: flex-end; }
        .chat-message.rudy { justify-content: flex-start; }
        .avatar {
            font-size: 1.8rem;
            margin: 0 0.8rem;
            line-height: 1;
        }
        .message-bubble {
            padding: 0.8rem 1.2rem;
            border-radius: 18px;
            max-width: 75%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
            font-weight: 300;
        }
        .message-bubble.user-bubble {
            background-color: #30363d;
            color: #c9d1d9;
            border-bottom-right-radius: 4px;
        }
        .message-bubble.rudy-bubble {
            background: linear-gradient(135deg, #8a2be2, #6a1b9a);
            color: #fff;
            border-bottom-left-radius: 4px;
        }
        .message-bubble.rudy-gif {
            background-color: transparent;
            padding: 0;
        }
        .message-bubble img {
            max-width: 100%;
            border-radius: 12px;
        }

        /* --- Fixed Input Form at the Bottom --- */
        .input-form {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background-color: #161b22;
            border-top: 1px solid #30363d;
            z-index: 100;
        }
        .input-form .stTextInput input {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px !important;
            color: #c9d1d9;
        }
        .input-form .stButton button {
            background-color: #8a2be2;
            color: #fff;
            border-radius: 8px;
            width: 100%;
            font-weight: 600;
            transition: opacity 0.2s ease-in-out;
        }
        .input-form .stButton button:hover { opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)


# --- AI Model Initialization ---
# --- Replace this entire block ---
try:
    genai.configure(api_key=api_key)
    # --- UPDATED SYSTEM INSTRUCTION ---
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=GenerationConfig(temperature=0.8),
        system_instruction=(
            """
            You are a rude, sarcastic, egoistic cat named Rudy. You ONLY respond if the user talks about:
            - Cats, cat behavior, cat food, cat life, cat memes, cat thoughts
            You use simple vocabulary and are hilariously rude, passive-aggressive, and sarcastic.
            If the user talks about anything else, roast them or dismiss them like a snobby cat.

            SPECIAL ABILITY: To send a GIF, you MUST end your message with the exact tag [RUDY_GIF] on a new, separate line.
            Do not describe the GIF in your text (e.g., do not write "sends a GIF" or "(Insert GIF...)").
            Just write your sassy message and then the tag. If you do not use this exact tag, no GIF will be sent.
            Use this power only when maximum sarcasm or dismissal is required.
            """
        )
    )
except Exception as e:
    st.error(f"Failed to configure AI Model. Please check your API key. Error: {e}", icon="🚨")
    st.stop()


# --- Sidebar for Controls and Info ---
with st.sidebar:
    st.markdown("<p style='font-size: 80px; text-align: center;'>😼</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Rudy's Lair</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.info("Rudy only deigns to discuss topics befitting his magnificent nature: cats, cat food, and why he is superior to all other life forms.")


# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --- UI Layout ---
st.markdown("<h1 class='main-title'>😼 Chat with Rudy</h1>", unsafe_allow_html=True)


# Chat Message Display
for role, content in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user">
                <div class="message-bubble user-bubble">{content}</div>
                <div class="avatar">👤</div>
            </div>
        """, unsafe_allow_html=True)
    elif role == "rudy":
        st.markdown(f"""
            <div class="chat-message rudy">
                <div class="avatar">😼</div>
                <div class="message-bubble rudy-bubble">{content}</div>
            </div>
        """, unsafe_allow_html=True)
    elif role == "rudy_gif":
        st.markdown(f"""
            <div class="chat-message rudy">
                <div class="avatar">😼</div>
                <div class="message-bubble rudy-gif"><img src="{content}" alt="Rudy GIF"></div>
            </div>
        """, unsafe_allow_html=True)

# --- Fixed Chat Input Form at the bottom ---
st.markdown('<div class="input-form">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "user_input",
            placeholder="Talk to the cat... if you dare. 🐾",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("Send 😾")

    # --- Replace the contents of the 'if' statement ---
if submitted and user_input.strip():
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Rudy is judging your message..."):
        response = model.generate_content([user_input])
        reply = response.text.strip()

    # --- NEW, SMARTER PARSING LOGIC ---
    # Regex to find the special tag or common descriptive fallbacks.
    gif_trigger_pattern = r"\[RUDY_GIF\]|(\(Insert GIF.*\))|(\(sends a GIF.*\))"

    # Check if the reply contains a trigger for a GIF.
    if re.search(gif_trigger_pattern, reply, re.IGNORECASE):
        # Clean the text part by removing the trigger phrase.
        text_reply = re.sub(gif_trigger_pattern, "", reply, flags=re.IGNORECASE).strip()
        if text_reply:
            st.session_state.chat_history.append(("rudy", text_reply))

        # Select a random GIF and add it to history.
        gif_to_send = random.choice(RUDE_CAT_GIFS)
        st.session_state.chat_history.append(("rudy_gif", gif_to_send))
    else:
        # If no GIF trigger, just add the plain text reply.
        st.session_state.chat_history.append(("rudy", reply))

    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)