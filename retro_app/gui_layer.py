"""
GUI Layer for Terminal Dialogue System
Handles Streamlit presentation and user interaction
"""
import streamlit as st
import os
from PIL import Image
from typing import List, Dict, Any, Optional
from data_layer import dialogue_manager
from logic_layer import game_state


def apply_terminal_style():
    """Apply the retro terminal CSS styling"""
    st.markdown("""
    <style>
    /* Base styling */
    body {
        margin: 0;
        padding: 0;
        background-color: #111;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Main container to position the CRT in the center */
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* CRT Monitor Bezel */
    .block-container {
        max-width: 1000px !important;
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 auto;
        position: relative;
    }
    
    /* CRT Screen Effect */
    .stApp {
        background-color: #000000;
        border-radius: 20px;
        border: 25px solid #333;
        box-shadow: 
            inset 0 0 10px rgba(0, 255, 0, 0.3),
            0 0 30px rgba(0, 255, 0, 0.1),
            0 10px 50px rgba(0, 0, 0, 0.8);
        position: relative;
        overflow: hidden;
        margin: 40px auto;
        width: 90% !important;
        max-width: 900px;
    }
    
    /* CRT monitor plastic frame */
    .stApp::before {
        content: "";
        position: absolute;
        top: -25px;
        left: -25px;
        right: -25px;
        bottom: -25px;
        background-color: #222;
        border-radius: 30px;
        border: 5px solid #111;
        z-index: -1;
    }
    
    /* CRT scanlines */
    .stApp::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            rgba(0, 0, 0, 0) 50%, 
            rgba(0, 0, 0, 0.15) 50%
        );
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 999;
    }
    
    /* Add CRT screen curvature */
    .stApp {
        border-radius: 20px;
        overflow: hidden;
    }
    
    /* CRT glare effect */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(
            ellipse at center,
            rgba(0, 20, 0, 0) 0%,
            rgba(0, 20, 0, 0.2) 80%,
            rgba(0, 20, 0, 0.3) 100%
        );
        pointer-events: none;
        z-index: 998;
    }
    
    /* Add power button to the frame */
    footer {
        position: fixed;
        right: calc(50% - 450px);
        bottom: 10px;
        z-index: 1000;
    }
    
    footer:after {
        content: "POWER";
        position: absolute;
        bottom: 25px;
        right: 25px;
        width: 60px;
        height: 30px;
        background-color: #222;
        border: 2px solid #111;
        border-radius: 5px;
        color: #555;
        font-size: 10px;
        text-align: center;
        line-height: 30px;
        cursor: pointer;
    }
    
    /* Buttons styling */
    .stButton>button {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
        width: 100%;
        text-align: left;
        padding: 10px;
        transition: background-color 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #003300;
        color: #00FF00;
    }
    
    /* Terminal text styling */
    .stTextInput>div>div>input {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #000000;
        color: #00FF00;
        border-left: 1px solid #00FF00;
    }
    
    /* Dialog text styling */
    .dialog-text {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        padding: 10px;
        font-family: 'Courier New', monospace;
        margin-bottom: 20px;
        position: relative;
        box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
    }
    
    .dialog-header {
        color: #FFFFFF;
        margin-bottom: 5px;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }
    
    /* Terminal cursor */
    .terminal-cursor {
        animation: blink 1s step-end infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* Conversation history */
    .history-entry {
        margin-bottom: 10px;
        border-bottom: 1px dashed #003300;
        padding-bottom: 10px;
    }
    
    /* Quest log styling */
    .quest-log {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        padding: 10px;
        margin-top: 20px;
        box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
    }
    
    /* Text flicker animation */
    @keyframes textFlicker {
        0% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.8); }
        5% { text-shadow: 0 0 10px rgba(0, 255, 0, 0.8); }
        10% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.8); }
        15% { text-shadow: 0 0 7px rgba(0, 255, 0, 0.8); }
        25% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.8); }
        30% { text-shadow: 0 0 8px rgba(0, 255, 0, 0.8); }
        70% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.8); }
        80% { text-shadow: 0 0 9px rgba(0, 255, 0, 0.8); }
        100% { text-shadow: 0 0 5px rgba(0, 255, 0, 0.8); }
    }
    
    .dialog-text, .dialog-header {
        animation: textFlicker 3s infinite;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with controls and information"""
    st.sidebar.markdown("<h2 style='color: #00FF00;'>SYSTEM CONTROLS</h2>", unsafe_allow_html=True)
    
    # Create a file selector for conversation files
    conversation_files = ["Select a conversation..."] + dialogue_manager.get_available_conversations()
    
    selected_conversation = st.sidebar.selectbox(
        "Load conversation", 
        conversation_files, 
        key="conversation_selector"
    )
    
    if selected_conversation != "Select a conversation...":
        try:
            file_path = os.path.join(dialogue_manager.conversations_directory, selected_conversation)
            if game_state.load_dialogue(file_path):
                st.sidebar.success(f"Loaded: {selected_conversation}")
                game_state.reset_state()
                st.rerun()
            else:
                st.sidebar.error(f"Failed to load {selected_conversation}")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {str(e)}")
    
    # Standard file uploader as alternative
    uploaded_file = st.sidebar.file_uploader(
        "Or upload dialogue data (JSON)", 
        type="json", 
        key="json_uploader"
    )
    
    if uploaded_file is not None:
        try:
            dialogue_data = dialogue_manager.load_dialogue_data(uploaded_file.name)
            game_state.dialogue_data = dialogue_data
            game_state.reset_state()
            st.sidebar.success("Dialogue data loaded successfully!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error loading uploaded file: {str(e)}")
    
    # Option to reload the default dialogue
    if st.sidebar.button("Reload Default Dialogue"):
        if game_state.load_dialogue("dialogue_data.json"):
            game_state.reset_state()
            st.sidebar.success("Default dialogue data reloaded!")
            st.rerun()
        else:
            st.sidebar.error("Failed to load default dialogue")
    
    # Quest log
    st.sidebar.markdown("<h2 style='color: #00FF00;'>QUEST LOG</h2>", unsafe_allow_html=True)
    
    quest_stages = game_state.get_current_quest_stages()
    if not quest_stages:
        st.sidebar.markdown("<div class='quest-log'>No active quests.</div>", unsafe_allow_html=True)
    
    for stage in quest_stages:
        if stage.get("completed", False):
            st.sidebar.markdown(
                f"<h3 style='color: #FFFF00;'>{stage['quest_title']} ✓</h3>", 
                unsafe_allow_html=True
            )
            st.sidebar.markdown("<div class='quest-log'>Completed!</div>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(
                f"<h3 style='color: #FFFF00;'>{stage['quest_title']}</h3>", 
                unsafe_allow_html=True
            )
            st.sidebar.markdown(
                f"<div class='quest-log'>{stage['stage_text']}</div>", 
                unsafe_allow_html=True
            )
    
    # Conversation history
    st.sidebar.markdown("<h2 style='color: #00FF00;'>CONVERSATION LOG</h2>", unsafe_allow_html=True)
    
    if st.sidebar.button("Clear History"):
        game_state.conversation_history = []
        st.rerun()
    
    for entry in game_state.conversation_history:
        speaker_color = "#FFFF00" if entry.get("is_player", False) else "#00FFFF"
        st.sidebar.markdown(
            f"<div class='history-entry'><span style='color: {speaker_color};'>{entry['speaker']}:</span> {entry['text']}</div>", 
            unsafe_allow_html=True
        )


def display_image(image_url: str):
    """Display an image from a URL or file path"""
    try:
        # For remote images
        if image_url.startswith("http"):
            st.image(image_url, width=250)
        # For local images
        else:
            image_path = os.path.join(os.path.dirname(__file__), image_url)
            image = Image.open(image_path)
            st.image(image, width=250)
    except Exception as e:
        st.error(f"Unable to load image: {e}")


def typewriter_text(text: str, speed: int = 10):
    """Display text with a typewriter effect"""
    typed_text = st.empty()
    for i in range(len(text) + 1):
        typed_text.markdown(
            f"<div class='dialog-text'>{text[:i]}▋</div>", 
            unsafe_allow_html=True
        )
        # In a real implementation, you'd add a delay here
        # But for the prototype, we'll skip that


def render_dialogue():
    """Render the current dialogue and its responses"""
    # Terminal header
    st.markdown(
        "<h1 style='color: #00FF00; text-align: center;'>TERMINAL ACCESS v2.47</h1>", 
        unsafe_allow_html=True
    )
    
    # Get current dialogue
    current_dialogue = game_state.get_current_dialogue()
    
    # Display current dialogue
    if current_dialogue:
        # Check if this is a new dialogue (not yet in history)
        is_new_dialogue = not game_state.conversation_history or game_state.conversation_history[-1]["id"] != current_dialogue["id"]
        
        # Create two columns for image and text if image is present
        if "image_url" in current_dialogue and current_dialogue["image_url"]:
            col1, col2 = st.columns([1, 3])
            with col1:
                display_image(current_dialogue["image_url"])
            with col2:
                st.markdown(
                    f"<div class='dialog-header'>{current_dialogue['npc']}</div>", 
                    unsafe_allow_html=True
                )
                if is_new_dialogue:
                    typewriter_text(current_dialogue["text"])
                else:
                    st.markdown(
                        f"<div class='dialog-text'>{current_dialogue['text']}</div>", 
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                f"<div class='dialog-header'>{current_dialogue['npc']}</div>", 
                unsafe_allow_html=True
            )
            if is_new_dialogue:
                typewriter_text(current_dialogue["text"])
            else:
                st.markdown(
                    f"<div class='dialog-text'>{current_dialogue['text']}</div>", 
                    unsafe_allow_html=True
                )
        
        # Show player responses
        for response in current_dialogue.get("responses", []):
            # Check if response should be shown based on its condition
            condition = response.get("condition")
            if condition and not game_state.evaluate_condition(condition):
                continue  # Skip responses that don't meet their conditions
                
            if st.button(response["text"], key=response["id"]):
                success, error = game_state.select_response(response["id"])
                if success:
                    st.rerun()
                else:
                    st.error(error)
    else:
        # No dialogue found
        st.markdown(
            "<div class='dialog-text'>CONNECTION TERMINATED OR DIALOGUE NOT FOUND.</div>", 
            unsafe_allow_html=True
        )
        
        if game_state.dialogue_data:
            # Show debug info
            st.markdown(
                f"<div class='dialog-text'>Current dialogue ID: {game_state.current_dialogue_id}</div>", 
                unsafe_allow_html=True
            )
            
            # List available dialogue IDs
            if "dialogues" in game_state.dialogue_data:
                dialogue_ids = [d["id"] for d in game_state.dialogue_data["dialogues"]]
                st.markdown(
                    f"<div class='dialog-text'>Available dialogue IDs: {', '.join(dialogue_ids)}</div>", 
                    unsafe_allow_html=True
                )
        
        # Restart button
        if st.button("Restart Conversation"):
            if game_state.dialogue_data:
                game_state.reset_state()
                st.rerun()


def initialize_streamlit():
    """Initialize Streamlit app and session state"""
    # Set page configuration
    st.set_page_config(
        page_title="Terminal Dialogue Simulator",
        page_icon="🖥️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply terminal styling
    apply_terminal_style()
    
    # Initialize session state for the first use
    if not game_state.dialogue_data:
        try:
            game_state.load_dialogue("dialogue_data.json")
        except Exception:
            # If default dialogue doesn't exist, create an empty one
            game_state.dialogue_data = dialogue_manager.create_empty_dialogue_data()
            game_state.reset_state()


def main():
    """Main entry point for the Terminal Dialogue Simulator"""
    initialize_streamlit()
    render_sidebar()
    render_dialogue()


if __name__ == "__main__":
    main()