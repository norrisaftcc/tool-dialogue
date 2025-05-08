# Dialogue Templates

This directory contains template and example files for the Terminal Dialogue Simulator:

## Main Templates

- `dialogue_default.json` - Minimal template file to start a new dialogue
- `dialogue_example_standardized.json` - A complete example following all best practices
- `dialogue_schema.json` - The JSON schema that defines valid dialogue format

## Test Files

These files demonstrate various aspects of the dialogue system and validator:

- `test_valid.json` - A completely valid dialogue file with proper structure
- `test_circular_reference.json` - Example of circular dialogue paths (A→B→C→A)
- `test_invalid_references.json` - Examples of broken dialogue and quest references
- `test_missing_fields.json` - Example with missing optional fields
- `test_naming_conventions.json` - Example of poor naming conventions
- `test_quest_issues.json` - Example of quest stage issues (non-sequential stages)

## Usage

To create a new dialogue file using a template:

```bash
cp templates/dialogue_default.json conversations/my_new_dialogue.json
```

Then edit the new file with your content.

Always validate your dialogue files before using them:

```bash
./dialogue_validator.py --file conversations/my_new_dialogue.json
```