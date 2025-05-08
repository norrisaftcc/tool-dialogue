import streamlit as st
import json
import os
import re
from PIL import Image
import base64
import io
import requests
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Terminal Dialogue Simulator",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply the retro CRT styling with 80s monitor frame and image support
def apply_terminal_style():
    # CSS for retro terminal look with CRT monitor frame and image support
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
        font-weight: bold;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
    }
    
    /* Speaker image styling */
    .speaker-image {
        border: 2px solid #00FF00;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        background-color: #000;
        max-width: 100%;
        height: auto;
    }
    
    .speaker-container {
        display: flex;
        margin-bottom: 20px;
    }
    
    .speaker-image-container {
        flex: 0 0 120px;
        margin-right: 15px;
    }
    
    .speaker-text-container {
        flex: 1;
        background-color: #000000;
        border: 1px solid #00FF00;
        padding: 10px;
        box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
    }
    
    /* Quest styling */
    .quest-update {
        background-color: #001100;
        color: #FFFF00;
        border: 1px solid #FFFF00;
        padding: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
        box-shadow: 0 0 5px rgba(255, 255, 0, 0.3);
    }
    
    /* History styling */
    .history-container {
        opacity: 0.7;
        margin-bottom: 20px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: #000000;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00FF00;
        border: 1px solid #00FF00;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00CC00;
    }
    
    /* Debug styling */
    .debug-info {
        font-size: 12px;
        color: #888;
        margin-top: 30px;
        padding: 10px;
        border: 1px dashed #444;
        background-color: #111;
    }
    
    /* ASCII art styling */
    pre {
        color: #00FF00;
        background-color: transparent;
        border: none;
        font-family: 'Courier New', monospace;
        margin: 0;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to load dialogue data
def load_dialogue_data(file_path=None):
    # If a file path is provided, use it
    if file_path:
        try:
            if isinstance(file_path, str):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                # Handle uploaded file
                return json.loads(file_path.getvalue())
        except Exception as e:
            st.error(f"Error loading dialogue file: {e}")
            return None
    
    # Otherwise, load the default dialogue file
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        default_path = os.path.join(script_dir, "dialogue_default.json")
        with open(default_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading default dialogue file: {e}")
        return None

# Function to get dialogue by ID
def get_dialogue_by_id(dialogue_data, dialogue_id):
    for dialogue in dialogue_data.get("dialogues", []):
        if dialogue["id"] == dialogue_id:
            return dialogue
    return None

# Function to get character image URL
def get_character_image(dialogue_data, dialogue):
    # First check if the dialogue node has an image_url
    if "image_url" in dialogue and dialogue["image_url"]:
        return dialogue["image_url"]
    
    # Then check if there's a characters section with an entry for this NPC
    if "characters" in dialogue_data:
        npc_name = dialogue["npc"]
        for char_id, char_data in dialogue_data["characters"].items():
            if char_data.get("name") == npc_name:
                return char_data.get("image_url")
    
    # Return None if no image found
    return None

# Function to display an image from URL
def display_image_from_url(image_url):
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Function to display dialogue with image
def display_dialogue_with_image(dialogue_data, dialogue):
    image_url = get_character_image(dialogue_data, dialogue)
    
    if image_url:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            image = display_image_from_url(image_url)
            if image:
                st.image(image, width=150, caption=dialogue["npc"])
        
        with col2:
            st.markdown(f"<div class='dialog-header'>{dialogue['npc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='dialog-text'>{dialogue['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='dialog-header'>{dialogue['npc']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='dialog-text'>{dialogue['text']}</div>", unsafe_allow_html=True)

# Function to handle quest updates
def handle_quest_update(dialogue_data, script, session_state):
    if not script:
        return
    
    # StartQuest_quest_id
    if script.startswith("StartQuest_"):
        quest_id = script.replace("StartQuest_", "")
        for quest in dialogue_data["quests"]:
            if quest["id"] == quest_id:
                # Add to active quests with initial stage
                session_state.active_quests[quest_id] = 1
                
                # Display quest start message
                quest_stage = next((stage for stage in quest["stages"] if stage["id"] == 1), None)
                if quest_stage:
                    st.markdown(f"""
                    <div class='quest-update'>
                        <strong>NEW QUEST: {quest['title']}</strong><br>
                        {quest_stage['journal_entry']}
                    </div>
                    """, unsafe_allow_html=True)
                break
    
    # UpdateQuest_quest_id_stage
    elif script.startswith("UpdateQuest_"):
        parts = script.replace("UpdateQuest_", "").split("_")
        if len(parts) >= 2:
            quest_id = parts[0]
            try:
                stage_id = int(parts[1])
                
                for quest in dialogue_data["quests"]:
                    if quest["id"] == quest_id and quest_id in session_state.active_quests:
                        # Update quest stage
                        session_state.active_quests[quest_id] = stage_id
                        
                        # Display quest update message
                        quest_stage = next((stage for stage in quest["stages"] if stage["id"] == stage_id), None)
                        if quest_stage:
                            st.markdown(f"""
                            <div class='quest-update'>
                                <strong>QUEST UPDATED: {quest['title']}</strong><br>
                                {quest_stage['journal_entry']}
                            </div>
                            """, unsafe_allow_html=True)
                        break
            except ValueError:
                pass
    
    # CompleteQuest_quest_id
    elif script.startswith("CompleteQuest_"):
        quest_id = script.replace("CompleteQuest_", "")
        
        for quest in dialogue_data["quests"]:
            if quest["id"] == quest_id and quest_id in session_state.active_quests:
                # Remove from active quests
                del session_state.active_quests[quest_id]
                
                # Display quest completion message
                st.markdown(f"""
                <div class='quest-update'>
                    <strong>QUEST COMPLETED: {quest['title']}</strong><br>
                    {quest['description']}
                </div>
                """, unsafe_allow_html=True)
                break

# Function to display quest log
def display_quest_log(dialogue_data, active_quests):
    if not active_quests:
        st.write("No active quests.")
        return
    
    for quest_id, stage_id in active_quests.items():
        for quest in dialogue_data["quests"]:
            if quest["id"] == quest_id:
                st.markdown(f"### {quest['title']}")
                st.write(quest['description'])
                
                # Find current stage
                quest_stage = next((stage for stage in quest["stages"] if stage["id"] == stage_id), None)
                if quest_stage:
                    st.markdown(f"**Current objective:** {quest_stage['journal_entry']}")
                
                st.markdown("---")
                break

# Main application
def main():
    # Apply styling
    apply_terminal_style()
    
    # Initialize session state
    if 'dialogue_data' not in st.session_state:
        st.session_state.dialogue_data = None
    if 'current_dialogue_id' not in st.session_state:
        st.session_state.current_dialogue_id = None
    if 'dialogue_history' not in st.session_state:
        st.session_state.dialogue_history = []
    if 'active_quests' not in st.session_state:
        st.session_state.active_quests = {}
    if 'show_debug' not in st.session_state:
        st.session_state.show_debug = False
    
    # Sidebar
    with st.sidebar:
        st.title("Terminal Controls")
        
        # File upload
        uploaded_file = st.file_uploader("Upload Dialogue File", type=['json'])
        
        if uploaded_file is not None:
            if st.button("Load Dialogue"):
                st.session_state.dialogue_data = load_dialogue_data(uploaded_file)
                if st.session_state.dialogue_data:
                    st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
                    st.session_state.dialogue_history = []
                    st.session_state.active_quests = {}
                    st.success("Dialogue file loaded successfully!")
        
        # Reset button
        if st.button("Reset Dialogue"):
            st.session_state.dialogue_data = None
            st.session_state.current_dialogue_id = None
            st.session_state.dialogue_history = []
            st.session_state.active_quests = {}
            st.success("Dialogue reset!")
        
        # Quest log
        st.markdown("## Quest Log")
        if st.session_state.dialogue_data:
            display_quest_log(st.session_state.dialogue_data, st.session_state.active_quests)
        
        # Debug toggle
        st.session_state.show_debug = st.checkbox("Show Debug Info", value=st.session_state.show_debug)
    
    # Main content
    st.title("Terminal Dialogue Simulator")
    
    # Load dialogue data if not already loaded
    if not st.session_state.dialogue_data:
        st.session_state.dialogue_data = load_dialogue_data()
        if st.session_state.dialogue_data:
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
    
    # Display dialogue
    if st.session_state.dialogue_data and st.session_state.current_dialogue_id:
        # Get current dialogue
        current_dialogue = get_dialogue_by_id(st.session_state.dialogue_data, st.session_state.current_dialogue_id)
        
        if current_dialogue:
            # Display dialogue history
            if st.session_state.dialogue_history:
                with st.expander("Conversation History", expanded=False):
                    for idx, history_item in enumerate(st.session_state.dialogue_history):
                        if "npc" in history_item:
                            st.markdown(f"**{history_item['npc']}:** {history_item['text']}")
                        else:
                            st.markdown(f"*{history_item['text']}*")
            
            # Display current dialogue with image
            display_dialogue_with_image(st.session_state.dialogue_data, current_dialogue)
            
            # Add to history
            if not st.session_state.dialogue_history or st.session_state.dialogue_history[-1].get("id") != current_dialogue["id"]:
                st.session_state.dialogue_history.append({
                    "id": current_dialogue["id"],
                    "npc": current_dialogue["npc"],
                    "text": current_dialogue["text"]
                })
            
            # Process any on_entry script
            if "on_entry" in current_dialogue and current_dialogue["on_entry"]:
                handle_quest_update(st.session_state.dialogue_data, current_dialogue["on_entry"], st.session_state)
            
            # Display response options
            if current_dialogue["responses"]:
                st.markdown("### Your Response:")
                
                for response in current_dialogue["responses"]:
                    if st.button(response["text"], key=response["id"]):
                        # Add to history
                        st.session_state.dialogue_history.append({
                            "text": response["text"],
                            "is_player": True
                        })
                        
                        # Process any script
                        if "script" in response and response["script"]:
                            handle_quest_update(st.session_state.dialogue_data, response["script"], st.session_state)
                        
                        # Set next dialogue
                        if response["next_dialogue"]:
                            st.session_state.current_dialogue_id = response["next_dialogue"]
                            st.experimental_rerun()
                        else:
                            st.markdown("**End of conversation.**")
                            if st.button("Start Over"):
                                st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
                                st.session_state.dialogue_history = []
                                st.experimental_rerun()
            else:
                st.markdown("**End of conversation.**")
                if st.button("Start Over"):
                    st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
                    st.session_state.dialogue_history = []
                    st.experimental_rerun()
        else:
            st.error(f"Dialogue with ID '{st.session_state.current_dialogue_id}' not found.")
    else:
        # Display intro message if no dialogue is loaded
        st.markdown("""
        <div class='dialog-text'>
        WELCOME TO THE TERMINAL DIALOGUE SIMULATOR
        
        To begin, upload a dialogue file or use the default one.
        
        Click "Start" to begin the conversation.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start"):
            if not st.session_state.dialogue_data:
                st.session_state.dialogue_data = load_dialogue_data()
            
            if st.session_state.dialogue_data:
                st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
                st.experimental_rerun()
    
    # Debug info
    if st.session_state.show_debug and st.session_state.dialogue_data:
        with st.expander("Debug Information", expanded=True):
            st.markdown("### Current Dialogue")
            st.write(f"ID: {st.session_state.current_dialogue_id}")
            
            current_dialogue = get_dialogue_by_id(st.session_state.dialogue_data, st.session_state.current_dialogue_id)
            if current_dialogue:
                st.write(f"NPC: {current_dialogue['npc']}")
                if "image_url" in current_dialogue:
                    st.write(f"Image URL: {current_dialogue['image_url']}")
                
                st.markdown("### Responses")
                for idx, response in enumerate(current_dialogue["responses"]):
                    st.write(f"{idx+1}. {response['text']} -> {response['next_dialogue']}")
                    if "script" in response and response["script"]:
                        st.write(f"   Script: {response['script']}")
                    if "condition" in response and response["condition"]:
                        st.write(f"   Condition: {response['condition']}")
            
            st.markdown("### Active Quests")
            st.write(st.session_state.active_quests)
            
            if "characters" in st.session_state.dialogue_data:
                st.markdown("### Characters")
                for char_id, char_data in st.session_state.dialogue_data["characters"].items():
                    st.write(f"{char_id}: {char_data.get('name')} - {char_data.get('image_url', 'No image')}")

if __name__ == "__main__":
    main()