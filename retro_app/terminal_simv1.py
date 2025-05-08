import streamlit as st
import json
import os
import re
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Terminal Dialogue Simulator",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply the 80s terminal retro styling
def apply_terminal_style():
    # CSS for retro terminal look
    st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
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
    .stTextInput>div>div>input {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
    }
    .stSidebar {
        background-color: #000000;
        color: #00FF00;
    }
    .css-1kyxreq {
        background-color: #000000;
        color: #00FF00;
    }
    .css-1kyxreq a {
        color: #00FFFF !important;
    }
    .dialog-text {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        padding: 10px;
        font-family: 'Courier New', monospace;
        margin-bottom: 20px;
        position: relative;
    }
    .dialog-header {
        color: #FFFFFF;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .terminal-cursor {
        animation: blink 1s step-end infinite;
    }
    @keyframes blink {
        50% { opacity: 0; }
    }
    .history-entry {
        margin-bottom: 10px;
        border-bottom: 1px dashed #003300;
        padding-bottom: 10px;
    }
    .quest-log {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        padding: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to load dialogue data from JSON file
def load_dialogue_data(file_path="dialogue_data.json"):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Dialogue data file '{file_path}' not found.")
        return {"dialogues": [], "quests": []}
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from '{file_path}'. Check the file format.")
        return {"dialogues": [], "quests": []}

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
        st.session_state.current_dialogue_id = "ai_escape_intro"
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "quest_state" not in st.session_state:
        st.session_state.quest_state = {}
    
    # Add file uploader for JSON data
    st.sidebar.markdown("<h2 style='color: #00FF00;'>SYSTEM CONTROLS</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.sidebar.file_uploader("Upload dialogue data (JSON)", type="json")
    if uploaded_file is not None:
        try:
            st.session_state.dialogue_data = json.load(uploaded_file)
            st.sidebar.success("Dialogue data loaded successfully!")
            # Reset conversation when new data is loaded
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_escape_intro")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
        except json.JSONDecodeError:
            st.sidebar.error("Error decoding JSON. Check file format.")
    
    # Option to reload the default dialogue
    if st.sidebar.button("Reload Default Dialogue"):
        st.session_state.dialogue_data = load_dialogue_data()
        st.session_state.current_dialogue_id = "ai_escape_intro"
        st.session_state.conversation_history = []
        st.session_state.quest_state = {}
        st.sidebar.success("Default dialogue data reloaded!")
    
    # Terminal header
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>TERMINAL ACCESS v2.47</h1>", unsafe_allow_html=True)
    
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
        
        if is_new_dialogue:
            st.markdown(f"<div class='dialog-header'>{current_dialogue['npc']}</div>", unsafe_allow_html=True)
            typewriter_text(current_dialogue["text"])
            
            # Add to history
            st.session_state.conversation_history.append({
                "id": current_dialogue["id"],
                "speaker": current_dialogue["npc"],
                "text": current_dialogue["text"],
                "is_player": False
            })
        else:
            # Just show the text without animation
            st.markdown(f"<div class='dialog-header'>{current_dialogue['npc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='dialog-text'>{current_dialogue['text']}</div>", unsafe_allow_html=True)
        
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
                if "script" in response:
                    handle_script(response["script"])
                
                # Move to next dialogue
                if response["next_dialogue"] is not None:
                    st.session_state.current_dialogue_id = response["next_dialogue"]
                
                # Rerun to update the UI
                st.rerun()
    else:
        st.markdown("<div class='dialog-text'>CONNECTION TERMINATED.</div>", unsafe_allow_html=True)
        if st.button("Restart Conversation"):
            st.session_state.current_dialogue_id = "ai_escape_intro"
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

# Support for importing Twine data (placeholder for now)
def import_twine_data(twine_content):
    # This would parse Twine data into our dialogue format
    # For the prototype, this is just a placeholder
    st.warning("Twine import functionality would go here.")
    return load_dialogue_data()  # For now, just return the default dialogue

# Run the application
if __name__ == "__main__":
    main()