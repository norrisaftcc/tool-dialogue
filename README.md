# Retro Terminal Dialogue System

A nostalgic green-on-black terminal dialogue simulator with branching conversations and a companion dialogue editor.

## Overview

This project provides a retro-style terminal dialogue system that mimics the look and feel of 1980s computer terminals. The system includes:

- **Terminal Dialogue Simulator**: An interactive interface for playing through dialogue trees
- **Dialogue Editor**: A tool for creating and modifying dialogue files
- **Standardized JSON Format**: A robust structure for dialogue data
- **CLI Parser**: A command-line interface for dialogue interaction

The 80s terminal aesthetic evokes a time when carefully staring at a menu before clicking was high gameplay.

## Getting Started

### Setup and Installation

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv streamlit_env
   source streamlit_env/bin/activate  # On Windows: streamlit_env\Scripts\activate
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Applications

1. **Running the Terminal Simulator**:
   ```bash
   streamlit run retro_app/terminal_simulator.py
   ```

2. **Running the Dialogue Editor**:
   ```bash
   streamlit run retro_app/dialogue_editor.py
   ```

3. **Using the CLI Parser** (for command-line interaction):
   ```bash
   python retro_app/cli_parser.py retro_app/dialogue_tutorial.json
   ```

## Using the Tutorial

The project includes a tutorial dialogue file that introduces the system's features:

1. **To load the tutorial in the simulator**:
   - Start the terminal simulator
   - Click "Upload Dialogue File" in the sidebar
   - Select `retro_app/dialogue_tutorial.json`
   - Click "Start" to begin the tutorial

2. **To run the tutorial in CLI mode**:
   ```bash
   python retro_app/cli_parser.py retro_app/dialogue_tutorial.json
   ```

The tutorial features a character named Pixel who guides you through:
- Basic navigation of dialogues
- The quest system
- Variables and conditions
- How to create your own dialogues

## Creating Your Own Dialogues

You can create your own dialogue scenarios in two ways:

1. **Using the Dialogue Editor**:
   - Run the dialogue editor application
   - Create dialogue nodes, responses, and quests through the interface
   - Save your creation as a JSON file

2. **Editing JSON Directly**:
   - Follow the format in `retro_app/README_standardized_format.md`
   - Use `retro_app/dialogue_example_standardized.json` as a template
   - Validate your file with the schema validator:
     ```bash
     python retro_app/schema_validator.py your_dialogue.json
     ```

## File Structure

- `retro_app/terminal_simulator.py` - Main application for the dialogue simulator
- `retro_app/dialogue_editor.py` - Editor for creating dialogue JSON files
- `retro_app/cli_parser.py` - Command-line interface for dialogue interaction
- `retro_app/schema_validator.py` - Tool for validating dialogue files
- `retro_app/dialogue_schema.json` - JSON schema definition
- `retro_app/*.json` - Various dialogue data files in JSON format
- `retro_app/README_*.md` - Documentation for different components

## Documentation

- `retro_app/README_dialogue_format.md` - Original dialogue format documentation
- `retro_app/README_standardized_format.md` - Standardized dialogue format specification
- `retro_app/README_dialogue_editor.md` - Guide to using the dialogue editor
- `retro_app/README_terminal_sim.md` - Guide to using the terminal simulator

## Example Dialogue Files

- `retro_app/dialogue_tutorial.json` - Interactive tutorial introducing the system
- `retro_app/dialogue_default.json` - Simple example with basic structure
- `retro_app/dialogue_example_standardized.json` - Example using the standardized format
- `retro_app/dialogue_data.json` - More complex dialogue scenario (AI escape)
- `retro_app/dialogue_datav2.json`, `retro_app/dialogue_datav3.json` - Alternative scenarios
- `retro_app/dialogue_about.json` - Meta-dialogue about the system itself