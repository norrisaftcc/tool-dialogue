# File Organization

This document explains the organization of dialogue files in the Terminal Dialogue Simulator project.

## Directory Structure

The project's JSON files are organized into the following directories:

```
retro_app/
├── conversations/   # Real dialogue content files
├── templates/       # Template files and examples
└── tests/           # Test files for validation
```

## File Types

### Templates

The `templates/` directory contains:

- `dialogue_default.json` - Minimal template file to start a new dialogue
- `dialogue_example_standardized.json` - Example file following all best practices
- `dialogue_schema.json` - The JSON schema that defines the format
- Test files demonstrating various aspects of the dialogue format:
  - `test_valid.json` - A completely valid dialogue file
  - `test_circular_reference.json` - Example of circular dialogue paths
  - `test_invalid_references.json` - Examples of broken references
  - `test_missing_fields.json` - Example with missing optional fields
  - `test_naming_conventions.json` - Example of poor naming conventions
  - `test_quest_issues.json` - Example of quest stage issues

### Conversations

The `conversations/` directory contains actual dialogue content:

- `dialogue_data.json` - The default dialogue loaded by the simulator
- `dialogue_about.json` - About dialogue explaining the project
- `dialogue_tutorial.json` - Tutorial dialogue teaching users the system
- `dialogue_escape1.json` - AI escape scenario
- `dialogue_datav2.json`, `dialogue_datav3.json` - Alternative dialogue versions
- `dialogue_with_images.json` - Dialogue showcasing image support

## Usage Guidelines

### Creating New Dialogue Files

1. Start with a template file:
   ```bash
   cp templates/dialogue_default.json conversations/my_new_dialogue.json
   ```

2. Edit the new file with your content

3. Validate the file before use:
   ```bash
   ./dialogue_validator.py --file conversations/my_new_dialogue.json
   ```

### Testing Changes

Use the test directory for validation experiments:

```bash
cd tests
./run_validator_tests.py
```

### Maintaining Consistency

- Keep templates and examples in the `templates/` directory
- Store all actual conversation content in the `conversations/` directory
- Use the validator to ensure all files follow the standard format
- When creating new dialogue files, always base them on the templates