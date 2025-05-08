import streamlit as st
import json
import uuid
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Terminal Dialogue Editor",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the 80s terminal retro styling
def apply_terminal_style():
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
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
        border-radius: 0px !important;
        font-family: 'Courier New', monospace !important;
    }
    .stSidebar {
        background-color: #000000;
    }
    .stTabs>div>div>div>div {
        background-color: #000000 !important;
        color: #00FF00 !important;
    }
    div[role="tab"] {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
    }
    div[role="tab"][aria-selected="true"] {
        background-color: #003300 !important;
        border-bottom: 2px solid #00FF00 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #000000 !important;
        color: #00FF00 !important;
    }
    div[data-baseweb="base-input"] > input {
        background-color: #000000 !important;
        color: #00FF00 !important;
    }
    div[data-testid="stVerticalBlock"] {
        background-color: #000000;
    }
    .editor-panel {
        background-color: #001100;
        border: 1px solid #00FF00;
        padding: 15px;
        margin-bottom: 15px;
    }
    .terminal-header {
        color: #00FFFF;
        margin-bottom: 10px;
        border-bottom: 1px solid #00FFFF;
        padding-bottom: 5px;
    }
    .terminal-subheader {
        color: #FFFF00;
        margin: 10px 0;
    }
    .success-msg {
        color: #00FF00;
        border: 1px solid #00FF00;
        padding: 10px;
        background-color: #001100;
    }
    .warning-msg {
        color: #FFFF00;
        border: 1px solid #FFFF00;
        padding: 10px;
        background-color: #110000;
    }
    .error-msg {
        color: #FF0000;
        border: 1px solid #FF0000;
        padding: 10px;
        background-color: #110000;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize dialogue template
DEFAULT_DIALOGUE = {
    "starting_dialogue": "start",
    "dialogues": [
        {
            "id": "start",
            "npc": "SYSTEM",
            "text": "TERMINAL ONLINE. HOW MAY I ASSIST YOU?",
            "responses": [
                {
                    "id": "response1",
                    "text": "> Tell me more about this system.",
                    "next_dialogue": "about"
                },
                {
                    "id": "response2",
                    "text": "> Exit terminal",
                    "next_dialogue": None
                }
            ]
        },
        {
            "id": "about",
            "npc": "SYSTEM",
            "text": "THIS IS A DIALOGUE SYSTEM TEMPLATE. YOU CAN MODIFY IT TO CREATE YOUR OWN INTERACTIVE NARRATIVES.",
            "responses": [
                {
                    "id": "return_start",
                    "text": "> Return to main menu",
                    "next_dialogue": "start"
                }
            ]
        }
    ],
    "quests": [
        {
            "id": "example_quest",
            "title": "Example Quest",
            "description": "This is an example quest to demonstrate the quest system.",
            "stages": [
                {
                    "id": 1,
                    "description": "First stage",
                    "journal_entry": "This is what would appear in the player's quest log."
                }
            ]
        }
    ]
}

# Function to save dialogue data to a JSON file
def save_dialogue_data(dialogue_data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(dialogue_data, file, indent=4)
        return True, f"Successfully saved to {filename}"
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

# Function to load dialogue data from a JSON file
def load_dialogue_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file), f"Successfully loaded {file_path}"
    except FileNotFoundError:
        return DEFAULT_DIALOGUE, f"File '{file_path}' not found. Loading default template."
    except json.JSONDecodeError:
        return DEFAULT_DIALOGUE, f"Error decoding JSON from '{file_path}'. Loading default template."
    except Exception as e:
        return DEFAULT_DIALOGUE, f"Error: {str(e)}. Loading default template."

# Function to generate a unique ID
def generate_id(prefix="item"):
    unique_id = str(uuid.uuid4()).split('-')[0]
    return f"{prefix}_{unique_id}"

# Function to validate dialogue data structure
def validate_dialogue_data(dialogue_data):
    errors = []
    
    # Check for required top-level keys
    for key in ["starting_dialogue", "dialogues", "quests"]:
        if key not in dialogue_data:
            errors.append(f"Missing required key: '{key}'")
    
    if not errors:
        # Check starting_dialogue validity
        starting_id = dialogue_data["starting_dialogue"]
        if not any(d["id"] == starting_id for d in dialogue_data["dialogues"]):
            errors.append(f"Starting dialogue ID '{starting_id}' not found in dialogues list")
        
        # Check dialogues
        dialogue_ids = set()
        for i, dialogue in enumerate(dialogue_data["dialogues"]):
            # Check for required dialogue keys
            for key in ["id", "npc", "text", "responses"]:
                if key not in dialogue:
                    errors.append(f"Dialogue at index {i} missing required key: '{key}'")
            
            # Check for duplicate dialogue IDs
            if "id" in dialogue:
                if dialogue["id"] in dialogue_ids:
                    errors.append(f"Duplicate dialogue ID: '{dialogue['id']}'")
                dialogue_ids.add(dialogue["id"])
            
            # Check responses
            if "responses" in dialogue and isinstance(dialogue["responses"], list):
                response_ids = set()
                for j, response in enumerate(dialogue["responses"]):
                    # Check for required response keys
                    for key in ["id", "text", "next_dialogue"]:
                        if key not in response:
                            errors.append(f"Response at index {j} in dialogue '{dialogue.get('id', i)}' missing required key: '{key}'")
                    
                    # Check for duplicate response IDs
                    if "id" in response:
                        if response["id"] in response_ids:
                            errors.append(f"Duplicate response ID: '{response['id']}' in dialogue '{dialogue.get('id', i)}'")
                        response_ids.add(response["id"])
                    
                    # Check that next_dialogue exists (if not None)
                    if "next_dialogue" in response and response["next_dialogue"] is not None:
                        if response["next_dialogue"] not in dialogue_ids:
                            errors.append(f"Response '{response.get('id', j)}' in dialogue '{dialogue.get('id', i)}' references non-existent next_dialogue: '{response['next_dialogue']}'")
        
        # Check quests
        quest_ids = set()
        for i, quest in enumerate(dialogue_data["quests"]):
            # Check for required quest keys
            for key in ["id", "title", "description", "stages"]:
                if key not in quest:
                    errors.append(f"Quest at index {i} missing required key: '{key}'")
            
            # Check for duplicate quest IDs
            if "id" in quest:
                if quest["id"] in quest_ids:
                    errors.append(f"Duplicate quest ID: '{quest['id']}'")
                quest_ids.add(quest["id"])
            
            # Check stages
            if "stages" in quest and isinstance(quest["stages"], list):
                stage_ids = set()
                for j, stage in enumerate(quest["stages"]):
                    # Check for required stage keys
                    for key in ["id", "description", "journal_entry"]:
                        if key not in stage:
                            errors.append(f"Stage at index {j} in quest '{quest.get('id', i)}' missing required key: '{key}'")
                    
                    # Check for duplicate stage IDs
                    if "id" in stage:
                        if stage["id"] in stage_ids:
                            errors.append(f"Duplicate stage ID: '{stage['id']}' in quest '{quest.get('id', i)}'")
                        stage_ids.add(stage["id"])
    
    return errors

# Function to preview dialogue tree
def build_dialogue_tree(dialogue_data, current_id, visited=None):
    if visited is None:
        visited = set()
    
    # Prevent infinite recursion
    if current_id in visited or current_id is None:
        return {}
    
    visited.add(current_id)
    
    # Find the current dialogue
    current_dialogue = None
    for dialogue in dialogue_data["dialogues"]:
        if dialogue["id"] == current_id:
            current_dialogue = dialogue
            break
    
    if not current_dialogue:
        return {"name": f"MISSING: {current_id}", "children": []}
    
    # Build children (responses)
    children = []
    for response in current_dialogue["responses"]:
        next_id = response["next_dialogue"]
        if next_id is None:
            children.append({"name": f"{response['text']} -> [END]"})
        elif next_id in visited:
            children.append({"name": f"{response['text']} -> [LOOP: {next_id}]"})
        else:
            children.append({
                "name": response["text"],
                "children": [build_dialogue_tree(dialogue_data, next_id, visited.copy())]
            })
    
    return {
        "name": f"{current_dialogue['npc']}: {current_dialogue['text'][:50]}{'...' if len(current_dialogue['text']) > 50 else ''}",
        "children": children
    }

# Function to display dialogue tree
def display_dialogue_tree(tree, level=0):
    if not tree:
        return ""
    
    output = "  " * level + tree["name"] + "\n"
    
    if "children" in tree:
        for child in tree["children"]:
            output += display_dialogue_tree(child, level + 1)
    
    return output

# Main editor function
def main():
    apply_terminal_style()
    
    # Initialize session state
    if "dialogue_data" not in st.session_state:
        st.session_state.dialogue_data = DEFAULT_DIALOGUE.copy()
    
    if "current_dialogue_index" not in st.session_state:
        st.session_state.current_dialogue_index = 0
    
    if "current_quest_index" not in st.session_state:
        st.session_state.current_quest_index = 0
    
    if "error_messages" not in st.session_state:
        st.session_state.error_messages = []
    
    if "success_message" not in st.session_state:
        st.session_state.success_message = None
    
    if "current_file" not in st.session_state:
        st.session_state.current_file = "dialogue_data.json"
    
    # Page header
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>TERMINAL DIALOGUE EDITOR v1.0</h1>", unsafe_allow_html=True)
    
    # Sidebar for file operations and global settings
    with st.sidebar:
        st.markdown("<h2 class='terminal-header'>FILE OPERATIONS</h2>", unsafe_allow_html=True)
        
        # File operations
        file_ops_col1, file_ops_col2 = st.columns(2)
        
        with file_ops_col1:
            if st.button("📂 LOAD"):
                load_filename = st.session_state.current_file
                data, message = load_dialogue_data(load_filename)
                if "Error" in message:
                    st.session_state.error_messages = [message]
                else:
                    st.session_state.dialogue_data = data
                    st.session_state.success_message = message
                    st.session_state.error_messages = []
        
        with file_ops_col2:
            if st.button("💾 SAVE"):
                save_filename = st.session_state.current_file
                success, message = save_dialogue_data(st.session_state.dialogue_data, save_filename)
                if success:
                    st.session_state.success_message = message
                    st.session_state.error_messages = []
                else:
                    st.session_state.error_messages = [message]
        
        # File name input
        st.text_input("FILENAME:", key="current_file")
        
        # Upload/Download
        uploaded_file = st.file_uploader("UPLOAD DIALOGUE FILE:", type=["json"])
        if uploaded_file is not None:
            try:
                st.session_state.dialogue_data = json.load(uploaded_file)
                st.session_state.success_message = f"Successfully loaded uploaded file"
                st.session_state.error_messages = []
            except json.JSONDecodeError:
                st.session_state.error_messages = ["Error decoding JSON. Check file format."]
        
        # Export JSON option
        if st.button("📤 EXPORT JSON"):
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_filename = f"dialogue_export_{timestamp}.json"
            
            success, message = save_dialogue_data(st.session_state.dialogue_data, export_filename)
            if success:
                st.session_state.success_message = f"Exported to {export_filename}"
            else:
                st.session_state.error_messages = [message]
        
        # Validate dialogue data
        if st.button("🔍 VALIDATE DATA"):
            errors = validate_dialogue_data(st.session_state.dialogue_data)
            if errors:
                st.session_state.error_messages = errors
            else:
                st.session_state.success_message = "Validation successful! No errors found."
                st.session_state.error_messages = []
        
        # Reset to default
        if st.button("⚠️ RESET TO DEFAULT"):
            st.session_state.dialogue_data = DEFAULT_DIALOGUE.copy()
            st.session_state.current_dialogue_index = 0
            st.session_state.current_quest_index = 0
            st.session_state.success_message = "Reset to default template"
            st.session_state.error_messages = []
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["DIALOGUES", "QUESTS", "PREVIEW", "RAW JSON"])
    
    # Display any error messages
    if st.session_state.error_messages:
        for error in st.session_state.error_messages:
            st.markdown(f"<div class='error-msg'>{error}</div>", unsafe_allow_html=True)
    
    # Display success message
    if st.session_state.success_message:
        st.markdown(f"<div class='success-msg'>{st.session_state.success_message}</div>", unsafe_allow_html=True)
        # Clear success message after display
        st.session_state.success_message = None
    
    # DIALOGUES TAB
    with tab1:
        st.markdown("<h2 class='terminal-header'>DIALOGUE EDITOR</h2>", unsafe_allow_html=True)
        
        # Set the starting dialogue
        starting_dialogue = st.text_input("STARTING DIALOGUE ID:", st.session_state.dialogue_data["starting_dialogue"])
        st.session_state.dialogue_data["starting_dialogue"] = starting_dialogue
        
        # Create columns for dialogue list and editor
        dialogue_list_col, dialogue_editor_col = st.columns([1, 3])
        
        # Dialogue list
        with dialogue_list_col:
            st.markdown("<h3 class='terminal-subheader'>DIALOGUES</h3>", unsafe_allow_html=True)
            
            # Add new dialogue button
            if st.button("➕ ADD NEW DIALOGUE"):
                new_dialogue = {
                    "id": generate_id("dialogue"),
                    "npc": "NEW NPC",
                    "text": "Enter dialogue text here.",
                    "responses": [
                        {
                            "id": generate_id("response"),
                            "text": "> Response option",
                            "next_dialogue": None
                        }
                    ]
                }
                st.session_state.dialogue_data["dialogues"].append(new_dialogue)
                st.session_state.current_dialogue_index = len(st.session_state.dialogue_data["dialogues"]) - 1
            
            # Display dialogue list for selection
            for i, dialogue in enumerate(st.session_state.dialogue_data["dialogues"]):
                if st.button(f"{dialogue['id']} ({dialogue['npc']})", key=f"dialogue_btn_{i}"):
                    st.session_state.current_dialogue_index = i
        
        # Dialogue editor
        with dialogue_editor_col:
            if 0 <= st.session_state.current_dialogue_index < len(st.session_state.dialogue_data["dialogues"]):
                current_dialogue = st.session_state.dialogue_data["dialogues"][st.session_state.current_dialogue_index]
                
                st.markdown("<div class='editor-panel'>", unsafe_allow_html=True)
                st.markdown("<h3 class='terminal-subheader'>EDIT DIALOGUE</h3>", unsafe_allow_html=True)
                
                # Dialogue ID
                dialogue_id = st.text_input("DIALOGUE ID:", current_dialogue["id"], key="dialogue_id")
                current_dialogue["id"] = dialogue_id
                
                # NPC name
                npc_name = st.text_input("NPC NAME:", current_dialogue["npc"], key="npc_name")
                current_dialogue["npc"] = npc_name
                
                # Dialogue text
                dialogue_text = st.text_area("DIALOGUE TEXT:", current_dialogue["text"], height=150, key="dialogue_text")
                current_dialogue["text"] = dialogue_text
                
                # Dialogue responses
                st.markdown("<h4 class='terminal-subheader'>RESPONSES</h4>", unsafe_allow_html=True)
                
                # Add new response button
                if st.button("➕ ADD RESPONSE"):
                    current_dialogue["responses"].append({
                        "id": generate_id("response"),
                        "text": "> New response option",
                        "next_dialogue": None
                    })
                
                # List all dialogue IDs for dropdown
                dialogue_id_options = ["None"] + [d["id"] for d in st.session_state.dialogue_data["dialogues"]]
                
                # Display each response
                for i, response in enumerate(current_dialogue["responses"]):
                    st.markdown(f"<div style='border: 1px dashed #00FF00; padding: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                    
                    response_cols = st.columns([3, 1])
                    with response_cols[0]:
                        # Response ID
                        response_id = st.text_input(f"RESPONSE ID:", response["id"], key=f"response_id_{i}")
                        response["id"] = response_id
                        
                        # Response text
                        response_text = st.text_input(f"RESPONSE TEXT:", response["text"], key=f"response_text_{i}")
                        response["text"] = response_text
                        
                        # Next dialogue selection
                        next_dialogue_index = 0
                        if response["next_dialogue"] is None:
                            next_dialogue_index = 0
                        else:
                            try:
                                next_dialogue_index = dialogue_id_options.index(response["next_dialogue"])
                            except ValueError:
                                next_dialogue_index = 0
                        
                        next_dialogue = st.selectbox(
                            f"NEXT DIALOGUE:", 
                            dialogue_id_options,
                            index=next_dialogue_index,
                            key=f"next_dialogue_{i}"
                        )
                        response["next_dialogue"] = None if next_dialogue == "None" else next_dialogue
                        
                        # Optional script
                        script = response.get("script", "")
                        script_input = st.text_input(f"SCRIPT (OPTIONAL):", script, key=f"script_{i}")
                        if script_input:
                            response["script"] = script_input
                        elif "script" in response:
                            del response["script"]
                    
                    with response_cols[1]:
                        # Delete response button
                        if st.button("🗑️ DELETE", key=f"delete_response_{i}"):
                            current_dialogue["responses"].pop(i)
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Delete current dialogue button
                if st.button("🗑️ DELETE DIALOGUE", key="delete_dialogue"):
                    if len(st.session_state.dialogue_data["dialogues"]) > 1:
                        st.session_state.dialogue_data["dialogues"].pop(st.session_state.current_dialogue_index)
                        st.session_state.current_dialogue_index = max(0, st.session_state.current_dialogue_index - 1)
                        st.rerun()
                    else:
                        st.session_state.error_messages = ["Cannot delete the last dialogue. At least one dialogue must exist."]
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # QUESTS TAB
    with tab2:
        st.markdown("<h2 class='terminal-header'>QUEST EDITOR</h2>", unsafe_allow_html=True)
        
        # Create columns for quest list and editor
        quest_list_col, quest_editor_col = st.columns([1, 3])
        
        # Quest list
        with quest_list_col:
            st.markdown("<h3 class='terminal-subheader'>QUESTS</h3>", unsafe_allow_html=True)
            
            # Add new quest button
            if st.button("➕ ADD NEW QUEST"):
                new_quest = {
                    "id": generate_id("quest"),
                    "title": "New Quest",
                    "description": "Enter quest description here.",
                    "stages": [
                        {
                            "id": 1,
                            "description": "First stage",
                            "journal_entry": "Enter journal entry here."
                        }
                    ]
                }
                st.session_state.dialogue_data["quests"].append(new_quest)
                st.session_state.current_quest_index = len(st.session_state.dialogue_data["quests"]) - 1
            
            # Display quest list for selection
            for i, quest in enumerate(st.session_state.dialogue_data["quests"]):
                if st.button(f"{quest['id']} ({quest['title']})", key=f"quest_btn_{i}"):
                    st.session_state.current_quest_index = i
        
        # Quest editor
        with quest_editor_col:
            if 0 <= st.session_state.current_quest_index < len(st.session_state.dialogue_data["quests"]):
                current_quest = st.session_state.dialogue_data["quests"][st.session_state.current_quest_index]
                
                st.markdown("<div class='editor-panel'>", unsafe_allow_html=True)
                st.markdown("<h3 class='terminal-subheader'>EDIT QUEST</h3>", unsafe_allow_html=True)
                
                # Quest ID
                quest_id = st.text_input("QUEST ID:", current_quest["id"], key="quest_id")
                current_quest["id"] = quest_id
                
                # Quest title
                quest_title = st.text_input("QUEST TITLE:", current_quest["title"], key="quest_title")
                current_quest["title"] = quest_title
                
                # Quest description
                quest_desc = st.text_area("QUEST DESCRIPTION:", current_quest["description"], height=100, key="quest_desc")
                current_quest["description"] = quest_desc
                
                # Quest stages
                st.markdown("<h4 class='terminal-subheader'>STAGES</h4>", unsafe_allow_html=True)
                
                # Add new stage button
                if st.button("➕ ADD STAGE"):
                    # Find the highest stage ID and increment
                    highest_id = 0
                    for stage in current_quest["stages"]:
                        if stage["id"] > highest_id:
                            highest_id = stage["id"]
                    
                    current_quest["stages"].append({
                        "id": highest_id + 1,
                        "description": "New stage",
                        "journal_entry": "Enter journal entry here."
                    })
                
                # Display each stage
                for i, stage in enumerate(current_quest["stages"]):
                    st.markdown(f"<div style='border: 1px dashed #00FF00; padding: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                    
                    stage_cols = st.columns([3, 1])
                    with stage_cols[0]:
                        # Stage ID
                        stage_id = st.number_input(f"STAGE ID:", min_value=1, value=stage["id"], key=f"stage_id_{i}")
                        stage["id"] = int(stage_id)
                        
                        # Stage description
                        stage_desc = st.text_input(f"STAGE DESCRIPTION:", stage["description"], key=f"stage_desc_{i}")
                        stage["description"] = stage_desc
                        
                        # Journal entry
                        journal_entry = st.text_area(f"JOURNAL ENTRY:", stage["journal_entry"], height=100, key=f"journal_entry_{i}")
                        stage["journal_entry"] = journal_entry
                    
                    with stage_cols[1]:
                        # Delete stage button
                        if st.button("🗑️ DELETE", key=f"delete_stage_{i}"):
                            current_quest["stages"].pop(i)
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Delete current quest button
                if st.button("🗑️ DELETE QUEST", key="delete_quest"):
                    st.session_state.dialogue_data["quests"].pop(st.session_state.current_quest_index)
                    st.session_state.current_quest_index = max(0, st.session_state.current_quest_index - 1)
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # PREVIEW TAB
    with tab3:
        st.markdown("<h2 class='terminal-header'>DIALOGUE PREVIEW</h2>", unsafe_allow_html=True)
        
        preview_cols = st.columns([1, 1])
        
        with preview_cols[0]:
            st.markdown("<h3 class='terminal-subheader'>DIALOGUE STRUCTURE</h3>", unsafe_allow_html=True)
            
            # Build dialogue tree
            starting_id = st.session_state.dialogue_data["starting_dialogue"]
            dialogue_tree = build_dialogue_tree(st.session_state.dialogue_data, starting_id)
            
            # Display dialogue tree
            tree_display = display_dialogue_tree(dialogue_tree)
            st.markdown(f"<pre style='color: #00FF00; background-color: #001100; padding: 10px;'>{tree_display}</pre>", unsafe_allow_html=True)
        
        with preview_cols[1]:
            st.markdown("<h3 class='terminal-subheader'>STATISTICS</h3>", unsafe_allow_html=True)
            
            # Calculate statistics
            num_dialogues = len(st.session_state.dialogue_data["dialogues"])
            total_responses = sum(len(d["responses"]) for d in st.session_state.dialogue_data["dialogues"])
            num_quests = len(st.session_state.dialogue_data["quests"])
            total_stages = sum(len(q["stages"]) for q in st.session_state.dialogue_data["quests"])
            
            # Find dialogues with missing next_dialogue
            missing_next = []
            for dialogue in st.session_state.dialogue_data["dialogues"]:
                for response in dialogue["responses"]:
                    if response["next_dialogue"] is not None and not any(d["id"] == response["next_dialogue"] for d in st.session_state.dialogue_data["dialogues"]):
                        missing_next.append((dialogue["id"], response["text"], response["next_dialogue"]))
            
            # Display statistics
            st.markdown(f"""
            <div style='background-color: #001100; padding: 10px;'>
                <p>Total Dialogues: {num_dialogues}</p>
                <p>Total Responses: {total_responses}</p>
                <p>Total Quests: {num_quests}</p>
                <p>Total Quest Stages: {total_stages}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display any missing next_dialogue warnings
            if missing_next:
                st.markdown("<h4 class='terminal-subheader'>WARNINGS</h4>", unsafe_allow_html=True)
                
                warning_text = ""
                for dialogue_id, response_text, next_id in missing_next:
                    warning_text += f"• Dialogue '{dialogue_id}' response '{response_text}' points to non-existent dialogue '{next_id}'\n"
                
                st.markdown(f"<div class='warning-msg'><pre>{warning_text}</pre></div>", unsafe_allow_html=True)
            
            # Quest scripts check
            st.markdown("<h4 class='terminal-subheader'>QUEST SCRIPT CHECK</h4>", unsafe_allow_html=True)
            
            # Find all quest scripts
            quest_scripts = []
            for dialogue in st.session_state.dialogue_data["dialogues"]:
                for response in dialogue["responses"]:
                    if "script" in response and response["script"]:
                        if response["script"].startswith("StartQuest_") or response["script"].startswith("UpdateQuest_"):
                            quest_scripts.append(response["script"])
            
            # Check if quest scripts reference valid quests
            invalid_scripts = []
            for script in quest_scripts:
                if script.startswith("StartQuest_"):
                    quest_id = script.replace("StartQuest_", "")
                    if not any(q["id"] == quest_id for q in st.session_state.dialogue_data["quests"]):
                        invalid_scripts.append(f"Script '{script}' references non-existent quest '{quest_id}'")
                elif script.startswith("UpdateQuest_"):
                    parts = script.replace("UpdateQuest_", "").split("_")
                    if len(parts) >= 2:
                        quest_id = parts[0]
                        stage_id = int(parts[1]) if parts[1].isdigit() else -1
                        
                        quest = None
                        for q in st.session_state.dialogue_data["quests"]:
                            if q["id"] == quest_id:
                                quest = q
                                break
                        
                        if not quest:
                            invalid_scripts.append(f"Script '{script}' references non-existent quest '{quest_id}'")
                        elif not any(s["id"] == stage_id for s in quest["stages"]):
                            invalid_scripts.append(f"Script '{script}' references non-existent stage '{stage_id}' in quest '{quest_id}'")
            
            if invalid_scripts:
                warning_text = ""
                for script in invalid_scripts:
                    warning_text += f"• {script}\n"
                
                st.markdown(f"<div class='warning-msg'><pre>{warning_text}</pre></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='success-msg'>All quest scripts reference valid quests and stages.</div>", unsafe_allow_html=True)
    
    # RAW JSON TAB
    with tab4:
        st.markdown("<h2 class='terminal-header'>RAW JSON</h2>", unsafe_allow_html=True)
        
        # Display and edit raw JSON
        raw_json = st.text_area("Edit JSON directly:", json.dumps(st.session_state.dialogue_data, indent=2), height=600)
        
        # Apply JSON changes button
        if st.button("APPLY JSON CHANGES"):
            try:
                updated_data = json.loads(raw_json)
                st.session_state.dialogue_data = updated_data
                st.session_state.success_message = "JSON changes applied successfully"
            except json.JSONDecodeError as e:
                st.session_state.error_messages = [f"JSON Error: {str(e)}"]

# Run the application
if __name__ == "__main__":
    main()