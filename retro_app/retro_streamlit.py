import streamlit as st
import random
import datetime

# Set page config
st.set_page_config(
    page_title="RetroComputer 8000",
    page_icon="🖥️",
    layout="centered"
)

# Apply custom CSS for 1980s retro look
st.markdown("""
<style>
    /* Global Retro Styling */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    /* Main container */
    .main {
        background-color: #000;
        color: #33ff33;
        font-family: 'VT323', monospace;
        border: 2px solid #33ff33;
        padding: 20px;
        border-radius: 5px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #33ff33 !important;
        font-family: 'VT323', monospace !important;
        text-shadow: 0 0 5px #33ff33;
    }
    
    /* Buttons */
    .stButton>button {
        font-family: 'VT323', monospace !important;
        background-color: #000 !important;
        color: #33ff33 !important;
        border: 2px solid #33ff33 !important;
        border-radius: 0 !important;
        box-shadow: 0 0 5px #33ff33 !important;
    }
    
    .stButton>button:hover {
        background-color: #33ff33 !important;
        color: #000 !important;
    }
    
    /* Text inputs */
    .stTextInput>div>div>input {
        font-family: 'VT323', monospace !important;
        background-color: #000 !important;
        color: #33ff33 !important;
        border: 2px solid #33ff33 !important;
        border-radius: 0 !important;
    }
    
    /* Sliders */
    .stSlider>div>div {
        color: #33ff33 !important;
    }
    
    /* Progress bar */
    .stProgress>div>div>div {
        background-color: #33ff33 !important;
    }
    
    /* Checkbox */
    .stCheckbox>div>div>label {
        color: #33ff33 !important;
    }
    
    /* Divider */
    hr {
        border-color: #33ff33 !important;
        box-shadow: 0 0 5px #33ff33 !important;
    }
    
    /* Custom retro terminal text */
    .terminal-text {
        display: inline-block;
        overflow: hidden;
        border-right: .15em solid #33ff33;
        white-space: nowrap;
        letter-spacing: .1em;
        animation: blink-caret .75s step-end infinite;
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #33ff33 }
    }
</style>
""", unsafe_allow_html=True)

# Header and intro
st.markdown("<h1>RetroComputer 8000</h1>", unsafe_allow_html=True)
st.markdown("<h2>BASIC System v1.0</h2>", unsafe_allow_html=True)
st.markdown("<p class='terminal-text'>READY.</p>", unsafe_allow_html=True)

# Display current date and time in retro format
now = datetime.datetime.now()
st.markdown(f"<p>DATE: {now.strftime('%Y-%m-%d')} | TIME: {now.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# Divider
st.markdown("<hr>", unsafe_allow_html=True)

# Create some retro-style interactive elements
st.markdown("<h3>SYSTEM CONTROLS</h3>", unsafe_allow_html=True)

# Memory slider
memory = st.slider("MEMORY ALLOCATION (KB)", 64, 640, 320)
st.markdown(f"<p>ALLOCATED: {memory} KB</p>", unsafe_allow_html=True)

# Progress bar to simulate system load
system_load = random.randint(10, 90)
st.markdown("<p>SYSTEM LOAD:</p>", unsafe_allow_html=True)
st.progress(system_load / 100)

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>INPUT MODULE</h3>", unsafe_allow_html=True)
    user_input = st.text_input("ENTER COMMAND:")
    
    if st.button("EXECUTE"):
        if user_input.lower() in ["help", "?", "commands"]:
            st.markdown("""
            <p>AVAILABLE COMMANDS:</p>
            <ul>
                <li>HELP - Display this help</li>
                <li>TIME - Display current time</li>
                <li>DATE - Display current date</li>
                <li>CALC - Simple calculator</li>
                <li>GAME - Play a game</li>
            </ul>
            """, unsafe_allow_html=True)
        elif user_input.lower() == "time":
            st.markdown(f"<p>CURRENT TIME: {now.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
        elif user_input.lower() == "date":
            st.markdown(f"<p>CURRENT DATE: {now.strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
        elif user_input.lower() == "calc":
            st.markdown("<p>CALCULATOR MODE ACTIVATED</p>", unsafe_allow_html=True)
            st.session_state.calculator = True
        elif user_input.lower() == "game":
            st.markdown("<p>LAUNCHING GAME MODULE...</p>", unsafe_allow_html=True)
            st.session_state.game = True
        else:
            st.markdown(f"<p>ERROR: UNKNOWN COMMAND '{user_input}'</p>", unsafe_allow_html=True)
            st.markdown("<p>TYPE 'HELP' FOR AVAILABLE COMMANDS</p>", unsafe_allow_html=True)

with col2:
    st.markdown("<h3>SYSTEM STATUS</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <ul>
        <li>CPU: Z80A @ 4MHz</li>
        <li>RAM: {memory} KB</li>
        <li>OS: RETROS v1.0</li>
        <li>STATUS: OPERATIONAL</li>
    </ul>
    """, unsafe_allow_html=True)
    
    # Checkboxes for system options
    st.markdown("<h4>OPTIONS</h4>", unsafe_allow_html=True)
    sound = st.checkbox("ENABLE SOUND")
    graphics = st.checkbox("ENABLE GRAPHICS")
    network = st.checkbox("ENABLE NETWORK")

# Calculator mode
if 'calculator' in st.session_state and st.session_state.calculator:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>CALCULATOR MODULE</h3>", unsafe_allow_html=True)
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        num1 = st.number_input("NUMBER 1:", min_value=0, max_value=999, value=0)
        
    with calc_col2:
        operation = st.selectbox("OPERATION:", ["+", "-", "*", "/"])
        num2 = st.number_input("NUMBER 2:", min_value=0, max_value=999, value=0)
    
    if st.button("CALCULATE"):
        result = 0
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/" and num2 != 0:
            result = num1 / num2
        elif operation == "/" and num2 == 0:
            st.markdown("<p>ERROR: DIVISION BY ZERO</p>", unsafe_allow_html=True)
            st.markdown("<p>SYSTEM HALT</p>", unsafe_allow_html=True)
            st.stop()
        
        st.markdown(f"<h4>RESULT: {result}</h4>", unsafe_allow_html=True)

# Game mode
if 'game' in st.session_state and st.session_state.game:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>GAME MODULE: NUMBER GUESSING</h3>", unsafe_allow_html=True)
    
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
    
    guess = st.number_input("YOUR GUESS (1-100):", min_value=1, max_value=100)
    
    if st.button("SUBMIT GUESS"):
        st.session_state.attempts += 1
        
        if guess < st.session_state.secret_number:
            st.markdown("<p>TOO LOW! TRY AGAIN.</p>", unsafe_allow_html=True)
        elif guess > st.session_state.secret_number:
            st.markdown("<p>TOO HIGH! TRY AGAIN.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4>CORRECT! YOU WIN IN {st.session_state.attempts} ATTEMPTS!</h4>", unsafe_allow_html=True)
            if st.button("PLAY AGAIN"):
                st.session_state.secret_number = random.randint(1, 100)
                st.session_state.attempts = 0

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p>(C) RETRO SYSTEMS INC. 1985</p>", unsafe_allow_html=True)
st.markdown("<p>MEMORY USAGE: 64K / BASIC BYTES FREE: 38911</p>", unsafe_allow_html=True)

