# Improving Dialogue Files

This document provides guidance on addressing common validation issues found in dialogue files.

## Understanding Validation Errors

When running the validator on existing files, you may see errors like:

```
❌ File: conversations/dialogue_example.json
   - In dialogue 'welcome', response 'ask_question' references non-existent dialogue 'answer'
   - In dialogue 'quest_start', response 'accept' script references non-existent quest 'main_quest'
```

These errors need to be addressed to ensure proper functioning of the dialogue system.

## Common Issues and Solutions

### 1. Broken Dialogue References

**Issue**: A response references a dialogue ID that doesn't exist.

```json
"next_dialogue": "nonexistent_dialogue"
```

**Solution**: 
- Create the missing dialogue node
- Change the reference to an existing dialogue node
- Set to `null` if the conversation should end

### 2. Missing Quest References

**Issue**: A script references a quest that isn't defined.

```json
"script": "StartQuest_missing_quest"
```

**Solution**:
- Create the quest in the "quests" array
- Update the script to reference an existing quest
- Remove the script if not needed

### 3. Schema Compliance

**Issue**: The file is missing required fields according to the schema.

**Solution**:
- Run the validator with the `--fix` option to add missing fields:
  ```bash
  ./dialogue_validator.py --file filename.json --fix
  ```

### 4. Circular References

**Issue**: Dialogues create a loop with no exit point.

**Solution**:
- Add a response option that exits the loop
- Ensure at least one path eventually leads to a dialogue with `next_dialogue: null`

## Standardizing Dialogue Files

To standardize all dialogue files:

1. Create a backup of your files

2. Run the validator in fix mode on each file:
   ```bash
   ./dialogue_validator.py --dir conversations/ --pattern "*.json" --fix --output-dir conversations_fixed/
   ```

3. Review the fixed files before replacing the originals

## Best Practices for Dialogue Creation

1. **Start from templates**: Always start new dialogue files from the standard templates

2. **Validate early and often**: Run the validator after making changes

3. **Use descriptive IDs**: Name dialogues and responses descriptively, e.g., `character_location_situation`

4. **Match references**: Ensure all dialogue references point to existing dialogues

5. **Complete quests**: Make sure quests have proper stages and are referenced correctly

6. **Document extensions**: If adding new script types or features, document them

## Working with Legacy Files

For legacy files with many issues:

1. Use the template creator to make a new standardized file:
   ```bash
   ./templates/create_new_dialogue.py --template dialogue_default.json --output my_new_dialogue.json --title "My Dialogue" --author "Your Name"
   ```

2. Copy existing content into the new structure

3. Update references and fix structural issues

4. Validate the new file before deployment