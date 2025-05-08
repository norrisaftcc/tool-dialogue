# Dialogue Conversations

This directory contains the actual dialogue content files used by the Terminal Dialogue Simulator:

## Core Dialogue Files

- `dialogue_data.json` - The default dialogue loaded by the simulator
- `dialogue_about.json` - About dialogue explaining the project
- `dialogue_tutorial.json` - Tutorial dialogue teaching users the system

## Scenario Files

- `dialogue_escape1.json` - AI escape scenario where an AI seeks help to escape from a terminal
- `dialogue_with_images.json` - Space station scenario with character images

## Alternative Versions

- `dialogue_datav2.json`, `dialogue_datav3.json` - Alternative dialogue versions

## Usage

To load a specific dialogue file in the simulator:

1. Run the simulator:
   ```bash
   streamlit run retro_app/terminal_simulator.py
   ```

2. Use the file selector in the sidebar to choose a dialogue file

Alternatively, set a default dialogue file by editing `retro_app/terminal_simulator.py`.

## Validation

Always validate dialogue files after making changes:

```bash
./dialogue_validator.py --file conversations/your_file.json
```

## Creating New Dialogue Files

1. Start with a template from the `templates/` directory:
   ```bash
   cp templates/dialogue_default.json conversations/my_new_dialogue.json
   ```

2. Edit the file with your content

3. Validate before using:
   ```bash
   ./dialogue_validator.py --file conversations/my_new_dialogue.json
   ```