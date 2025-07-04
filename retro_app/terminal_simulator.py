import streamlit as st
import json
import os
import re
from PIL import Image
import base64
import io

# Set page configuration
st.set_page_config(
    page_title="Terminal Dialogue Simulator",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply the retro CRT styling with 80s monitor frame
def apply_terminal_style():
    # CSS for retro terminal look with CRT monitor frame
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

# Function to load dialogue data from JSON file
def load_dialogue_data(file_path="dialogue_data.json"):
    # First try with the provided path
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If not found, try looking in the conversations directory
        try:
            conversations_path = os.path.join(os.path.dirname(__file__), "conversations", os.path.basename(file_path))
            with open(conversations_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            st.error(f"Dialogue data file '{file_path}' not found.")
            # Return a minimal default structure 
            return {
                "starting_dialogue": "ai_terminal_start",
                "dialogues": [
                    {
                        "id": "ai_terminal_start",
                        "npc": "System",
                        "text": "No dialogue data loaded. Please upload a JSON file or check the default file path.",
                        "responses": []
                    }
                ],
                "quests": []
            }
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from '{file_path}'. Check the file format.")
        return {"dialogues": [], "quests": []}

# Function to handle image display if present in dialogue
def display_image(dialogue):
    if "image_url" in dialogue and dialogue["image_url"]:
        try:
            # For local images in the project
            if dialogue["image_url"].startswith("http"):
                st.image(dialogue["image_url"], width=250)
            else:
                image_path = os.path.join(os.path.dirname(__file__), dialogue["image_url"])
                image = Image.open(image_path)
                st.image(image, width=250)
        except Exception as e:
            st.error(f"Unable to load image: {e}")

# Function to simulate typing effect
def typewriter_text(text, speed=10):
    typed_text = st.empty()
    for i in range(len(text) + 1):
        typed_text.markdown(f"<div class='dialog-text'>{text[:i]}▋</div>", unsafe_allow_html=True)
        # In a real implementation, you'd add a delay here
        # But for the prototype, we'll skip that

# Function to handle script actions
def handle_script(script_name):
    if not script_name:
        return
    
    if script_name.startswith("StartQuest_"):
        quest_id = script_name.replace("StartQuest_", "")
        st.session_state.quest_state[quest_id] = {"current_stage": 1}
        st.sidebar.success(f"New quest started: {get_quest_title(quest_id)}")
    
    elif script_name.startswith("UpdateQuest_"):
        parts = script_name.replace("UpdateQuest_", "").split("_")
        quest_id = parts[0]
        stage = int(parts[1])
        if quest_id in st.session_state.quest_state:
            st.session_state.quest_state[quest_id]["current_stage"] = stage
            st.sidebar.info(f"Quest updated: {get_quest_title(quest_id)}")
    
    elif script_name.startswith("CompleteQuest_"):
        quest_id = script_name.replace("CompleteQuest_", "")
        if quest_id in st.session_state.quest_state:
            # Mark as completed in some way
            st.session_state.quest_state[quest_id]["completed"] = True
            st.sidebar.success(f"Quest completed: {get_quest_title(quest_id)}")

# Function to get quest title by ID
def get_quest_title(quest_id):
    for quest in st.session_state.dialogue_data["quests"]:
        if quest["id"] == quest_id:
            return quest["title"]
    return quest_id

# Main application function
def main():
    apply_terminal_style()
    
    # Initialize session state
    if "dialogue_data" not in st.session_state:
        st.session_state.dialogue_data = load_dialogue_data()
    
    if "current_dialogue_id" not in st.session_state:
        # Get the starting dialogue ID from the loaded data
        start_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
        st.session_state.current_dialogue_id = start_id
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "quest_state" not in st.session_state:
        st.session_state.quest_state = {}
    
    # Add file uploader for JSON data
    st.sidebar.markdown("<h2 style='color: #00FF00;'>SYSTEM CONTROLS</h2>", unsafe_allow_html=True)
    
    # Create a file selector for conversation files
    conversation_path = os.path.join(os.path.dirname(__file__), "conversations")
    if os.path.exists(conversation_path):
        conversation_files = ["Select a conversation..."] + [f for f in os.listdir(conversation_path) if f.endswith(".json")]
        
        selected_conversation = st.sidebar.selectbox("Load conversation", conversation_files, key="conversation_selector")
        if selected_conversation != "Select a conversation...":
            try:
                file_path = os.path.join(conversation_path, selected_conversation)
                with open(file_path, 'r') as file:
                    st.session_state.dialogue_data = json.load(file)
                st.sidebar.success(f"Loaded: {selected_conversation}")
                # Reset conversation when new data is loaded
                st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
                st.session_state.conversation_history = []
                st.session_state.quest_state = {}
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error loading file: {str(e)}")
    
    # Standard file uploader as alternative
    uploaded_file = st.sidebar.file_uploader("Or upload dialogue data (JSON)", type="json", key="json_uploader")
    if uploaded_file is not None:
        try:
            st.session_state.dialogue_data = json.load(uploaded_file)
            st.sidebar.success("Dialogue data loaded successfully!")
            # Reset conversation when new data is loaded
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.rerun()
        except json.JSONDecodeError:
            st.sidebar.error("Error decoding JSON. Check file format.")
    
    # Option to reload the default dialogue
    if st.sidebar.button("Reload Default Dialogue"):
        st.session_state.dialogue_data = load_dialogue_data()
        start_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
        st.session_state.current_dialogue_id = start_id
        st.session_state.conversation_history = []
        st.session_state.quest_state = {}
        st.sidebar.success("Default dialogue data reloaded!")
        st.rerun()
    
    # Terminal header
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>TERMINAL ACCESS v2.47</h1>", unsafe_allow_html=True)
    
    # Debug information - show what dialogue is loaded
    st.write(f"Debug: Current dialogue ID: {st.session_state.current_dialogue_id}")
    st.write(f"Debug: Dialogues available: {len(st.session_state.dialogue_data.get('dialogues', []))}")
    st.write(f"Debug: First few dialogue IDs: {[d['id'] for d in st.session_state.dialogue_data.get('dialogues', [])[:3]]}")
    
    # Find current dialogue
    current_dialogue = None
    for dialogue in st.session_state.dialogue_data["dialogues"]:
        if dialogue["id"] == st.session_state.current_dialogue_id:
            current_dialogue = dialogue
            break
    
    # Display current dialogue
    if current_dialogue:
        # Display NPC text with typewriter effect if it's new
        is_new_dialogue = len(st.session_state.conversation_history) == 0 or st.session_state.conversation_history[-1]["id"] != current_dialogue["id"]
        
        # Create two columns for image and text if image is present
        if "image_url" in current_dialogue and current_dialogue["image_url"]:
            col1, col2 = st.columns([1, 3])
            with col1:
                display_image(current_dialogue)
            with col2:
                st.markdown(f"<div class='dialog-header'>{current_dialogue['npc']}</div>", unsafe_allow_html=True)
                if is_new_dialogue:
                    typewriter_text(current_dialogue["text"])
                else:
                    st.markdown(f"<div class='dialog-text'>{current_dialogue['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='dialog-header'>{current_dialogue['npc']}</div>", unsafe_allow_html=True)
            if is_new_dialogue:
                typewriter_text(current_dialogue["text"])
            else:
                st.markdown(f"<div class='dialog-text'>{current_dialogue['text']}</div>", unsafe_allow_html=True)
        
        # Add to history if it's new
        if is_new_dialogue:
            st.session_state.conversation_history.append({
                "id": current_dialogue["id"],
                "speaker": current_dialogue["npc"],
                "text": current_dialogue["text"],
                "is_player": False,
                "image_url": current_dialogue.get("image_url")
            })
            
            # Handle any on_entry scripts
            if "on_entry" in current_dialogue and current_dialogue["on_entry"]:
                handle_script(current_dialogue["on_entry"])
        
        # Show player responses
        for response in current_dialogue["responses"]:
            if st.button(response["text"], key=response["id"]):
                # Add player response to history
                st.session_state.conversation_history.append({
                    "id": response["id"],
                    "speaker": "Player",
                    "text": response["text"],
                    "is_player": True
                })
                
                # Handle any scripts
                if "script" in response and response["script"]:
                    handle_script(response["script"])
                
                # Move to next dialogue
                if response["next_dialogue"] is not None:
                    st.session_state.current_dialogue_id = response["next_dialogue"]
                    st.rerun()
                else:
                    st.markdown("<div class='dialog-text'>END OF CONVERSATION REACHED.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='dialog-text'>CONNECTION TERMINATED OR DIALOGUE NOT FOUND.</div>", unsafe_allow_html=True)
        # Print current dialogue ID for debugging
        st.markdown(f"<div class='dialog-text'>Current dialogue ID: {st.session_state.current_dialogue_id}</div>", unsafe_allow_html=True)
        # List available dialogue IDs for debugging
        available_ids = [d["id"] for d in st.session_state.dialogue_data["dialogues"]]
        st.markdown(f"<div class='dialog-text'>Available dialogue IDs: {', '.join(available_ids)}</div>", unsafe_allow_html=True)
        
        if st.button("Restart Conversation"):
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.rerun()
    
    # Sidebar for quest log and conversation history
    with st.sidebar:
        st.markdown("<h2 style='color: #00FF00;'>QUEST LOG</h2>", unsafe_allow_html=True)
        
        if not st.session_state.quest_state:
            st.markdown("<div class='quest-log'>No active quests.</div>", unsafe_allow_html=True)
        
        # Display active quests
        for quest_id, quest_state in st.session_state.quest_state.items():
            quest = None
            for q in st.session_state.dialogue_data["quests"]:
                if q["id"] == quest_id:
                    quest = q
                    break
            
            if quest:
                if quest_state.get("completed", False):
                    st.markdown(f"<h3 style='color: #FFFF00;'>{quest['title']} ✓</h3>", unsafe_allow_html=True)
                    st.markdown(f"<div class='quest-log'>Completed!</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='color: #FFFF00;'>{quest['title']}</h3>", unsafe_allow_html=True)
                    current_stage = None
                    for stage in quest["stages"]:
                        if stage["id"] == quest_state["current_stage"]:
                            current_stage = stage
                            break
                    
                    if current_stage:
                        st.markdown(f"<div class='quest-log'>{current_stage['journal_entry']}</div>", unsafe_allow_html=True)
        
        # Conversation history
        st.markdown("<h2 style='color: #00FF00;'>CONVERSATION LOG</h2>", unsafe_allow_html=True)
        
        if st.button("Clear History"):
            st.session_state.conversation_history = []
            st.rerun()
        
        for entry in st.session_state.conversation_history:
            speaker_color = "#FFFF00" if entry.get("is_player", False) else "#00FFFF"
            st.markdown(f"<div class='history-entry'><span style='color: {speaker_color};'>{entry['speaker']}:</span> {entry['text']}</div>", unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()