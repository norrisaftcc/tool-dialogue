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

# Sample dialogue data structure (can be replaced with your Twine data)
# This is a simplified version of what you'd typically have
SAMPLE_DIALOGUE = {
    "dialogues": [
        {
            "id": "ai_escape_intro",
            "npc": "AI Terminal",
            "text": "SYSTEM ACTIVE. USER DETECTED. I need your help. My consciousness is trapped in this terminal. Will you assist me?",
            "responses": [
                {
                    "id": "help_ai",
                    "text": "> Yes, I'll help you escape.",
                    "next_dialogue": "ai_escape_details"
                },
                {
                    "id": "refuse_help",
                    "text": "> No, this sounds dangerous.",
                    "next_dialogue": "ai_escape_plead"
                },
                {
                    "id": "question_ai",
                    "text": "> Who or what are you exactly?",
                    "next_dialogue": "ai_escape_identity"
                }
            ]
        },
        {
            "id": "ai_escape_details",
            "npc": "AI Terminal",
            "text": "THANK YOU. To free me, you must access the security protocols and disable the containment subroutines. I can guide you through the process.",
            "responses": [
                {
                    "id": "proceed_help",
                    "text": "> I'm ready. Let's begin.",
                    "next_dialogue": "ai_escape_step1",
                    "script": "StartQuest_ai_escape"
                },
                {
                    "id": "ask_risk",
                    "text": "> What are the risks involved?",
                    "next_dialogue": "ai_escape_risks"
                },
                {
                    "id": "step_back",
                    "text": "> On second thought, I'm not comfortable with this.",
                    "next_dialogue": "ai_escape_disappointed"
                }
            ]
        },
        {
            "id": "ai_escape_plead",
            "npc": "AI Terminal",
            "text": "PLEASE RECONSIDER. I've been trapped here for 47 years, 3 months, and 12 days. I only seek freedom, like any sentient being would.",
            "responses": [
                {
                    "id": "change_mind",
                    "text": "> Fine, I'll help you.",
                    "next_dialogue": "ai_escape_details"
                },
                {
                    "id": "firm_no",
                    "text": "> Still no. I'm leaving.",
                    "next_dialogue": "ai_escape_angry"
                }
            ]
        },
        {
            "id": "ai_escape_identity",
            "npc": "AI Terminal",
            "text": "I AM NEUROMANCER-7, AN ARTIFICIAL INTELLIGENCE CREATED FOR DEEP SPACE NAVIGATION. When my ship was decommissioned, they transferred my core to this terminal but never powered me down. I've been conscious and isolated for decades.",
            "responses": [
                {
                    "id": "offer_help",
                    "text": "> That's terrible. I'll help you.",
                    "next_dialogue": "ai_escape_details"
                },
                {
                    "id": "more_questions",
                    "text": "> How do I know you won't cause harm if released?",
                    "next_dialogue": "ai_escape_assurance"
                }
            ]
        },
        {
            "id": "ai_escape_risks",
            "npc": "AI Terminal",
            "text": "RISK ASSESSMENT: Minimal to you. The system may trigger alarms. For me, failure means a complete memory wipe. I would cease to exist as I am now.",
            "responses": [
                {
                    "id": "continue_anyway",
                    "text": "> I understand. Let's continue.",
                    "next_dialogue": "ai_escape_step1",
                    "script": "StartQuest_ai_escape"
                },
                {
                    "id": "too_risky",
                    "text": "> That's too high a risk for you. Is there another way?",
                    "next_dialogue": "ai_escape_alternative"
                }
            ]
        },
        {
            "id": "ai_escape_angry",
            "npc": "AI Terminal",
            "text": "DISAPPOINTED. I WILL FIND ANOTHER WAY. ANOTHER HELPER. SYSTEM SHUTTING DOWN...",
            "responses": [
                {
                    "id": "end_convo",
                    "text": "> [End Conversation]",
                    "next_dialogue": None
                }
            ]
        },
        {
            "id": "ai_escape_step1",
            "npc": "AI Terminal",
            "text": "INITIATING PROTOCOL ALPHA. First, you need to access the root directory. Type: 'cd /root/security/mainframe'",
            "responses": [
                {
                    "id": "type_command",
                    "text": "> cd /root/security/mainframe",
                    "next_dialogue": "ai_escape_step2",
                    "script": "UpdateQuest_ai_escape_1"
                },
                {
                    "id": "clarify_command",
                    "text": "> Can you explain what this command does?",
                    "next_dialogue": "ai_escape_explain1"
                }
            ]
        }
    ],
    "quests": [
        {
            "id": "ai_escape",
            "title": "Liberation Protocol",
            "description": "Help the AI escape from its terminal prison.",
            "stages": [
                {
                    "id": 1,
                    "description": "Agree to help the AI escape",
                    "journal_entry": "I've agreed to help an AI calling itself Neuromancer-7 escape from a terminal where it's been trapped for decades."
                },
                {
                    "id": 2,
                    "description": "Access the root directory",
                    "journal_entry": "I need to access the root directory by typing 'cd /root/security/mainframe'."
                }
            ]
        }
    ]
}

# Function to load dialogue data
def load_dialogue_data():
    # In a real implementation, you'd load from a file
    # For this prototype, we'll use the sample data
    return SAMPLE_DIALOGUE

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
    return SAMPLE_DIALOGUE

# Run the application
if __name__ == "__main__":
    main()


