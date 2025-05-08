# Retro Terminal Dialogue System - Presentation Outline

## Slide 1: Title
- **Title**: Retro Terminal Dialogue System
- **Subtitle**: Interactive Narrative Creation in a Nostalgic Interface
- *[Image: Screenshot of terminal with green text on black background]*

## Slide 2: Overview
- What is the Retro Terminal Dialogue System?
- Key components:
  - Terminal Simulator
  - Dialogue Editor
  - Standardized JSON Format
  - CLI Parser
- *[Image: Split screen showing editor and simulator]*

## Slide 3: Inspiration
- 1980s text adventures
- Command line aesthetics
- Modern interactive fiction tools
- Nostalgia meets modern functionality
- *[Images: Screenshots of Zork, early text adventures]*

## Slide 4: System Architecture
- Diagram showing component relationships
  - JSON Files ⟷ Dialogue Editor ⟶ Terminal Simulator
  - JSON Schema ⟶ Validator ⟶ JSON Files
  - CLI Parser ⟷ JSON Files
- *[Diagram: Flow chart of components]*

## Slide 5: Dialogue Format
- Standardized JSON structure
- Example of dialogue node:
```json
{
  "id": "ai_escape_intro",
  "npc": "AI Terminal",
  "text": "SYSTEM ACTIVE. USER DETECTED...",
  "responses": [
    {
      "id": "help_ai",
      "text": "> Yes, I'll help you escape.",
      "next_dialogue": "ai_escape_details",
      "script": null
    }
  ]
}
```
- *[Image: JSON structure visualization]*

## Slide 6: Key Features
- Branching dialogue trees
- Quest system
- Variables and conditions
- Script commands
- Multi-platform accessibility
- *[Images: Screenshots showing different features]*

## Slide 7: Terminal Simulator
- Green-on-black retro aesthetic
- Typewriter text effect
- Interactive dialogue choices
- Quest tracking
- *[Image: Screenshot of dialogue in action]*

## Slide 8: Dialogue Editor
- Visual creation interface
- Tabs for different aspects
  - Dialogues
  - Quests
  - Preview
  - Raw JSON
- *[Image: Screenshot of editor interface]*

## Slide 9: Schema Validation
- Ensures dialogue file correctness
- Validates references and relationships
- Suggests fixes for common issues
- Auto-upgrades legacy formats
- *[Image: Screenshot of validator output]*

## Slide 10: CLI Parser
- Command-line interface for dialogues
- Enables LLM interaction and testing
- Supports all dialogue features
- Platform-independent
- *[Image: Screenshot of CLI in action]*

## Slide 11: Use Cases
- Interactive fiction
- Game prototyping
- Training scenarios
- Educational content
- Chatbot testing
- *[Images: Examples of different applications]*

## Slide 12: Technical Implementation
- Built with:
  - Python backend
  - Streamlit for web UI
  - JSON Schema for validation
  - ANSI color codes for CLI
- *[Logos: Python, Streamlit, JSON]*

## Slide 13: Future Enhancements
- Variable system for state tracking
- Character/NPC attribute system
- Inventory system integration
- Visual dialogue tree editor
- Media integration (images, sound)
- *[Image: Mockup of future features]*

## Slide 14: Demo
- Live demonstration
- Try it yourself:
  - Web: `streamlit run retro_app/terminal_simulator.py`
  - CLI: `python retro_app/cli_parser.py dialogue_file.json`
- *[QR code linking to repository]*

## Slide 15: Questions
- Contact information
- Repository link
- Documentation references
- *[Image: Terminal with "READY FOR INPUT" prompt]*