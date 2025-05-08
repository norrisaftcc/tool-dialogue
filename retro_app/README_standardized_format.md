# Standardized Dialogue Format

This document outlines the standardized JSON format for dialogue files used in the Terminal Dialogue Simulator. This format is designed to be backward compatible with existing files while providing a more robust structure for future development.

## Schema Structure

The standard dialogue file format consists of these main sections:

```json
{
  "schema_version": "1.0",
  "metadata": { ... },
  "starting_dialogue": "start_id",
  "dialogues": [ ... ],
  "quests": [ ... ],
  "variables": { ... }
}
```

### Top-Level Properties

| Property | Required | Type | Description |
|----------|----------|------|-------------|
| `schema_version` | No | String | Version of the schema format (e.g., "1.0") |
| `metadata` | No | Object | Information about the dialogue file itself |
| `starting_dialogue` | Yes | String | ID of the first dialogue to display |
| `dialogues` | Yes | Array | Collection of dialogue objects |
| `quests` | Yes | Array | Collection of quest objects |
| `variables` | No | Object | Global state variables and their default values |

### Metadata Object

```json
"metadata": {
  "title": "Escape from Terminal",
  "author": "J. Smith",
  "creation_date": "2025-05-07",
  "description": "An AI trapped in a terminal seeks your help to escape"
}
```

### Dialogue Objects

Each dialogue represents a single interaction node:

```json
{
  "id": "ai_escape_intro",
  "npc": "AI Terminal",
  "text": "SYSTEM ACTIVE. USER DETECTED. I need your help.",
  "responses": [ ... ],
  "on_entry": "StartMusic_tense"
}
```

| Property | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | String | Unique identifier for the dialogue |
| `npc` | Yes | String | Character or system name speaking |
| `text` | Yes | String | Content of the dialogue |
| `responses` | Yes | Array | Possible player responses |
| `on_entry` | No | String or null | Script to run when dialogue is shown |

### Response Objects

Each response represents a player choice:

```json
{
  "id": "help_ai",
  "text": "> Yes, I'll help you escape.",
  "next_dialogue": "ai_escape_details",
  "script": "StartQuest_ai_escape",
  "condition": "HasItem_security_card"
}
```

| Property | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | String | Unique identifier for the response |
| `text` | Yes | String | Text displayed for this option |
| `next_dialogue` | Yes | String or null | ID of next dialogue or null to end |
| `script` | No | String or null | Script command to execute |
| `condition` | No | String or null | Condition for showing this response |

### Quest Objects

Quests represent objectives or storylines:

```json
{
  "id": "ai_escape",
  "title": "Liberation Protocol",
  "description": "Help the AI escape from its terminal prison.",
  "stages": [ ... ],
  "rewards": {
    "xp": 100,
    "items": ["security_pass", "ai_chip"]
  }
}
```

| Property | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | String | Unique identifier for the quest |
| `title` | Yes | String | Title displayed in quest log |
| `description` | Yes | String | Brief description of the quest |
| `stages` | Yes | Array | Progression stages of the quest |
| `rewards` | No | Object | Items/XP given on completion |

### Quest Stage Objects

Each quest has multiple stages:

```json
{
  "id": 1,
  "description": "Initial agreement",
  "journal_entry": "I've agreed to help an AI escape its terminal.",
  "on_complete": "GiveItem_access_code"
}
```

| Property | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | Yes | Integer | Stage number (starts at 1) |
| `description` | Yes | String | Internal description |
| `journal_entry` | Yes | String | Text shown in quest log |
| `on_complete` | No | String or null | Script executed when stage completes |

### Variables Object

Global variables with default values:

```json
"variables": {
  "has_met_ai": false,
  "trust_level": 0,
  "security_attempts": 0
}
```

## Naming Conventions

### Dialogue IDs
- Use descriptive names with underscores
- Format: `[character/location]_[purpose]_[state]`
- Example: `ai_escape_intro`, `terminal_security_locked`

### Response IDs
- Use descriptive names with underscores
- Format: `[action]_[target]` or `[reaction]_[detail]`
- Example: `help_ai`, `refuse_offer`, `ask_question`

### Script Commands
- Use PascalCase for actions with underscores separating parameters
- Format: `Action_Target_Parameters`
- Example: `StartQuest_ai_escape`, `UpdateQuest_escape_mission_2`

### Condition Commands
- Use the same format as script commands
- Example: `HasItem_keycard`, `QuestActive_main_mission`

## Best Practices

1. **Always include script fields** even if null to maintain consistency
   ```json
   "script": null
   ```

2. **Use semantic IDs** rather than generic numbers
   ```
   // Good
   "id": "ai_escape_intro"
   
   // Avoid
   "id": "dialogue1"
   ```

3. **Prefix player responses** with "> " for visual clarity
   ```json
   "text": "> I'll help you escape."
   ```

4. **Use null for conversation endings** rather than empty response arrays
   ```json
   "next_dialogue": null
   ```

5. **Start quest stage IDs at 1** and increment sequentially

6. **Include version information** to help with format migrations
   ```json
   "schema_version": "1.0"
   ```

## Script Commands Reference

### Quest Commands
- `StartQuest_quest_id`: Begin a new quest
- `UpdateQuest_quest_id_stage_number`: Update quest to specific stage
- `CompleteQuest_quest_id`: Mark a quest as completed

### Variable Commands
- `SetVariable_var_name_value`: Set a variable to a value
- `ModifyVariable_var_name_amount`: Modify variable by amount

### Condition Commands
- `HasItem_item_id`: Player has specific item
- `QuestActive_quest_id`: Quest is currently active
- `QuestStage_quest_id_stage`: Quest is at specific stage
- `VariableEquals_var_name_value`: Variable matches specific value
- `VariableGreaterThan_var_name_value`: Variable exceeds value
- `VariableLessThan_var_name_value`: Variable is below value

## Upgrading Legacy Files

To upgrade existing dialogue files to the new format:

1. Add `schema_version` and optional `metadata`
2. Ensure all response objects have `script` fields (use `null` if none)
3. Replace empty response arrays with a single "exit" response with `next_dialogue: null`
4. Standardize naming conventions for new content

Legacy files will continue to work without these changes, but updating to the new format is recommended for consistency and future compatibility.