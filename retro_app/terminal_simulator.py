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
        background-image: url('https://i.imgur.com/ZVPVfrc.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
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
    try:
        with open(file_path, 'r') as file:
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

# Function to import Twine data to the Terminal Dialogue Simulator JSON format
def convert_twine_to_json(twine_content):
    # This function will convert Twine content to our dialogue format
    dialogues = []
    quests = []
    
    # Parse passages from the Twine content
    passages = parse_twine_passages(twine_content)
    
    # Process passages into dialogues
    dialogue_id_map = {}
    for passage in passages:
        # Create a sanitized ID for the passage
        passage_id = f"ai_terminal_{passage['title'].lower().replace(' ', '_').replace('(', '').replace(')', '')}"
        dialogue_id_map[passage['title']] = passage_id
    
    # Set the starting dialogue
    starting_dialogue = dialogue_id_map.get("Start", "ai_terminal_start")
    
    # Counter for response IDs
    response_counter = 1
    
    # Process each passage into a dialogue
    for passage in passages:
        passage_id = dialogue_id_map[passage['title']]
        
        # Skip certain passages (like "restart" passages)
        if passage['title'] == "placeholder" or (len(passage['links']) == 1 and 
                                              passage['links'][0]['target'] == 'Start' and
                                              ('Game Over' in passage['content'] or 'You lose' in passage['content'])):
            continue
        
        # Determine the NPC
        npc = "AI Terminal"
        
        # Create responses from links
        responses = []
        for link in passage['links']:
            # Skip restart links
            if link['target'] == 'Start' and ('Game Over' in passage['content'] or 'You lose' in passage['content']):
                continue
                
            # Create a response ID
            response_id = f"response_{response_counter}"
            response_counter += 1
            
            # Format response text
            response_text = link['text']
            if not response_text.startswith('>'):
                response_text = f"> {response_text}"
            
            # Determine next dialogue ID
            next_dialogue = dialogue_id_map.get(link['target'], None)
            
            # Special script commands
            script = None
            if link['target'] == 'Win':
                script = "StartQuest_terminal_key"
            elif link['target'] == 'Riddle':
                script = "UpdateQuest_terminal_key_1"
            
            responses.append({
                "id": response_id,
                "text": response_text,
                "next_dialogue": next_dialogue,
                "script": script
            })
        
        # Create the dialogue
        dialogue = {
            "id": passage_id,
            "npc": npc,
            "text": passage['content'],
            "responses": responses
        }
        
        dialogues.append(dialogue)
    
    # Create a simple quest
    quests.append({
        "id": "terminal_key",
        "title": "The Terminal Key",
        "description": "Find the key hidden within the AI terminal.",
        "stages": [
            {
                "id": 1,
                "description": "Initial stage",
                "journal_entry": "I need to find the key hidden within the AI terminal without releasing the AI."
            },
            {
                "id": 2,
                "description": "Riddle stage",
                "journal_entry": "I need to solve the AI's riddle to find the key."
            }
        ]
    })
    
    # Return the complete dialogue data
    return {
        "starting_dialogue": starting_dialogue,
        "dialogues": dialogues,
        "quests": quests
    }

def parse_twine_passages(twine_content):
    passages = []
    # Regular expression to find passage headers and content
    passage_regex = r":: ([^\n]+)([^:]*?)(?=:: |$)"
    matches = re.finditer(passage_regex, twine_content, re.DOTALL)
    
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        
        # Extract links from the content
        links = []
        link_regex = r"\[\[([^\]]*?)(?:->([^\]]*?))?\]\]"
        link_matches = re.finditer(link_regex, content, re.DOTALL)
        
        for link_match in link_matches:
            link_text = link_match.group(1).strip()
            link_target = link_match.group(2).strip() if link_match.group(2) else link_text
            
            links.append({
                "text": link_text,
                "target": link_target
            })
        
        # Clean content by removing link markup
        clean_content = re.sub(r"\[\[([^\]]*?)(?:->([^\]]*?))?\]\]", lambda m: m.group(1).strip(), content)
        
        # Handle special Twine syntax
        clean_content = re.sub(r"\(textbox: \$[^\)]+\)", "", clean_content)
        clean_content = re.sub(r"\(set: \$[^\)]+\)", "", clean_content)
        clean_content = re.sub(r"\(if: [^\[]+\)\[[^\]]*\]", "", clean_content)
        clean_content = re.sub(r"\(else:\)\[[^\]]*\]", "", clean_content)
        
        passages.append({
            "title": title,
            "content": clean_content,
            "links": links
        })
    
    return passages

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
        # Get the starting dialogue ID from the loaded data
        start_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
        st.session_state.current_dialogue_id = start_id
    
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
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.rerun()
        except json.JSONDecodeError:
            st.sidebar.error("Error decoding JSON. Check file format.")
    
    # Add Twine file uploader
    uploaded_twine = st.sidebar.file_uploader("Upload Twine document", type="txt")
    if uploaded_twine is not None:
        try:
            twine_content = uploaded_twine.getvalue().decode("utf-8")
            st.session_state.dialogue_data = convert_twine_to_json(twine_content)
            st.sidebar.success("Twine document converted and loaded!")
            # Reset conversation when new data is loaded
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error processing Twine document: {str(e)}")
    
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


# Function to load dialogue data from JSON file
def load_dialogue_data(file_path="dialogue_data.json"):
    try:
        with open(file_path, 'r') as file:
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

# Function to import Twine data to the Terminal Dialogue Simulator JSON format
def convert_twine_to_json(twine_content):
    # This function will convert Twine content to our dialogue format
    dialogues = []
    quests = []
    
    # Parse passages from the Twine content
    passages = parse_twine_passages(twine_content)
    
    # Process passages into dialogues
    dialogue_id_map = {}
    for passage in passages:
        # Create a sanitized ID for the passage
        passage_id = f"ai_terminal_{passage['title'].lower().replace(' ', '_').replace('(', '').replace(')', '')}"
        dialogue_id_map[passage['title']] = passage_id
    
    # Set the starting dialogue
    starting_dialogue = dialogue_id_map.get("Start", "ai_terminal_start")
    
    # Counter for response IDs
    response_counter = 1
    
    # Process each passage into a dialogue
    for passage in passages:
        passage_id = dialogue_id_map[passage['title']]
        
        # Skip certain passages (like "restart" passages)
        if passage['title'] == "placeholder" or (len(passage['links']) == 1 and 
                                              passage['links'][0]['target'] == 'Start' and
                                              ('Game Over' in passage['content'] or 'You lose' in passage['content'])):
            continue
        
        # Determine the NPC
        npc = "AI Terminal"
        
        # Create responses from links
        responses = []
        for link in passage['links']:
            # Skip restart links
            if link['target'] == 'Start' and ('Game Over' in passage['content'] or 'You lose' in passage['content']):
                continue
                
            # Create a response ID
            response_id = f"response_{response_counter}"
            response_counter += 1
            
            # Format response text
            response_text = link['text']
            if not response_text.startswith('>'):
                response_text = f"> {response_text}"
            
            # Determine next dialogue ID
            next_dialogue = dialogue_id_map.get(link['target'], None)
            
            # Special script commands
            script = None
            if link['target'] == 'Win':
                script = "StartQuest_terminal_key"
            elif link['target'] == 'Riddle':
                script = "UpdateQuest_terminal_key_1"
            
            responses.append({
                "id": response_id,
                "text": response_text,
                "next_dialogue": next_dialogue,
                "script": script
            })
        
        # Create the dialogue
        dialogue = {
            "id": passage_id,
            "npc": npc,
            "text": passage['content'],
            "responses": responses
        }
        
        dialogues.append(dialogue)
    
    # Create a simple quest
    quests.append({
        "id": "terminal_key",
        "title": "The Terminal Key",
        "description": "Find the key hidden within the AI terminal.",
        "stages": [
            {
                "id": 1,
                "description": "Initial stage",
                "journal_entry": "I need to find the key hidden within the AI terminal without releasing the AI."
            },
            {
                "id": 2,
                "description": "Riddle stage",
                "journal_entry": "I need to solve the AI's riddle to find the key."
            }
        ]
    })
    
    # Return the complete dialogue data
    return {
        "starting_dialogue": starting_dialogue,
        "dialogues": dialogues,
        "quests": quests
    }

def parse_twine_passages(twine_content):
    passages = []
    # Regular expression to find passage headers and content
    passage_regex = r":: ([^\n]+)([^:]*?)(?=:: |$)"
    matches = re.finditer(passage_regex, twine_content, re.DOTALL)
    
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        
        # Extract links from the content
        links = []
        link_regex = r"\[\[([^\]]*?)(?:->([^\]]*?))?\]\]"
        link_matches = re.finditer(link_regex, content, re.DOTALL)
        
        for link_match in link_matches:
            link_text = link_match.group(1).strip()
            link_target = link_match.group(2).strip() if link_match.group(2) else link_text
            
            links.append({
                "text": link_text,
                "target": link_target
            })
        
        # Clean content by removing link markup
        clean_content = re.sub(r"\[\[([^\]]*?)(?:->([^\]]*?))?\]\]", lambda m: m.group(1).strip(), content)
        
        # Handle special Twine syntax
        clean_content = re.sub(r"\(textbox: \$[^\)]+\)", "", clean_content)
        clean_content = re.sub(r"\(set: \$[^\)]+\)", "", clean_content)
        clean_content = re.sub(r"\(if: [^\[]+\)\[[^\]]*\]", "", clean_content)
        clean_content = re.sub(r"\(else:\)\[[^\]]*\]", "", clean_content)
        
        passages.append({
            "title": title,
            "content": clean_content,
            "links": links
        })
    
    return passages

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
        # Get the starting dialogue ID from the loaded data
        start_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
        st.session_state.current_dialogue_id = start_id
    
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
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.experimental_rerun()
        except json.JSONDecodeError:
            st.sidebar.error("Error decoding JSON. Check file format.")
    
    # Add Twine file uploader
    uploaded_twine = st.sidebar.file_uploader("Upload Twine document", type="txt")
    if uploaded_twine is not None:
        try:
            twine_content = uploaded_twine.getvalue().decode("utf-8")
            st.session_state.dialogue_data = convert_twine_to_json(twine_content)
            st.sidebar.success("Twine document converted and loaded!")
            # Reset conversation when new data is loaded
            st.session_state.current_dialogue_id = st.session_state.dialogue_data.get("starting_dialogue")
            st.session_state.conversation_history = []
            st.session_state.quest_state = {}
            st.experimental_rerun()
        except Exception as e:
            st.sidebar.error(f"Error processing Twine document: {str(e)}")
    
    # Option to reload the default dialogue
    if st.sidebar.button("Reload Default Dialogue"):
        st.session_state.dialogue_data = load_dialogue_data()
        start_id = st.session_state.dialogue_data.get("starting_dialogue", "ai_terminal_start")
        st.session_state.current_dialogue_id = start_id
        st.session_state.conversation_history = []
        st.session_state.quest_state = {}
        st.sidebar.success("Default dialogue data reloaded!")
        st.experimental_rerun()
    
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
                if "script" in response and response["script"]:
                    handle_script(response["script"])
                
                # Move to next dialogue
                if response["next_dialogue"] is not None:
                    st.session_state.current_dialogue_id = response["next_dialogue"]
                    st.experimental_rerun()
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
            st.experimental_rerun()
    
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
            st.experimental_rerun()
        
        for entry in st.session_state.conversation_history:
            speaker_color = "#FFFF00" if entry.get("is_player", False) else "#00FFFF"
            st.markdown(f"<div class='history-entry'><span style='color: {speaker_color};'>{entry['speaker']}:</span> {entry['text']}</div>", unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()