# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project contains a retro-style terminal dialogue simulator and editor built with Streamlit. The application allows users to create, edit, and interact with dialogue trees in a nostalgic green-on-black terminal interface.

The project consists of two main components:
1. **Terminal Dialogue Simulator** - An interactive simulator that displays dialogue trees with branching conversation options
2. **Dialogue Editor** - A companion tool for creating and editing dialogue JSON files

## Commands

### Setup and Installation

```bash
# Create and activate virtual environment
python -m venv streamlit_env
source streamlit_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Applications

```bash
# Run the terminal simulator
streamlit run retro_app/terminal_simulator.py

# Run the dialogue editor
streamlit run retro_app/dialogue_editor.py
```

## Project Structure

- `retro_app/terminal_simulator.py` - Main application for the dialogue simulator
- `retro_app/dialogue_editor.py` - Editor for creating dialogue JSON files
- `retro_app/*.json` - Various dialogue data files in JSON format
- `retro_app/README_*.md` - Documentation for different components

## Key Files

- `dialogue_data.json` - The default dialogue data file
- `dialogue_datav2.json`, `dialogue_datav3.json` - Different versions of dialogue data
- `dialogue_escape1.json` - Specific dialogue scenario for an escape sequence

## Application Architecture

### Dialogue Format

The dialogue system uses a JSON format with the following structure:
- `starting_dialogue` - ID of the first dialogue to display
- `dialogues` - Array of dialogue objects with NPC text and player responses
- `quests` - Array of quest objects with stages and journal entries

Each dialogue node contains:
- Unique ID
- NPC name
- Display text
- Array of possible player responses

Each response contains:
- Unique ID
- Display text
- Next dialogue ID to navigate to
- Optional script commands (like starting quests)

Refer to `README_dialogue_format.md` for detailed documentation of the JSON structure.

### Simulator Features

- Retro terminal aesthetic with green text on black background
- Interactive dialogue system with player choices
- Quest tracking system
- Support for loading custom dialogue files
- Debug information for troubleshooting

### Editor Features

- Four main tabs: Dialogues, Quests, Preview, and Raw JSON
- Complete dialogue management (create, edit, delete)
- File operations (load, save, import, export)
- Visualization of dialogue tree structure
- Validation to catch dialogue errors

## Development Notes

- The application styling uses custom CSS to create the retro terminal look
- Streamlit's session state is used to track dialogue progression
- JSON data is loaded dynamically with error handling for invalid files
- Both applications support custom file uploads for flexibility