# README_dialogue_format.md

# Terminal Dialogue Simulator JSON Format Documentation

This document outlines the JSON format used by the Terminal Dialogue Simulator application. The format is designed to be flexible, human-readable, and easily editable either manually or through the companion Dialogue Editor application.

## Top-Level Structure

The JSON file has three required top-level elements:

```json
{
  "starting_dialogue": "start_id",
  "dialogues": [ ... array of dialogue objects ... ],
  "quests": [ ... array of quest objects ... ]
}
```

### starting_dialogue
A string that references the ID of the first dialogue to display when the simulator starts. This ID must match an existing dialogue in the `dialogues` array.

## Dialogue Objects

Each dialogue represents a single interaction node in the conversation tree:

```json
{
  "id": "unique_dialogue_id",
  "npc": "Character Name",
  "text": "The text displayed to the player for this dialogue node.",
  "responses": [ ... array of response objects ... ]
}
```

### id
A unique string identifier for the dialogue. IDs should:
- Be unique across all dialogues
- Contain only alphanumeric characters, underscores, and hyphens
- Be descriptive of the dialogue content (e.g., "ai_escape_intro")

### npc
The name of the non-player character or system that is speaking in this dialogue.

### text
The content of the dialogue that will be displayed to the player.

### responses
An array containing all possible player responses to this dialogue.

## Response Objects

Each response represents a player choice:

```json
{
  "id": "unique_response_id",
  "text": "> The text of the player's response",
  "next_dialogue": "next_dialogue_id",
  "script": "Optional_Script_Command"
}
```

### id
A unique string identifier for this response.

### text
The text of the response that will be shown to the player as a button. Conventionally starts with "> " to indicate a player response.

### next_dialogue
The ID of the dialogue that should be displayed after this response is selected. Can be `null` to end the conversation.

### script (optional)
A string representing a script command to execute when this response is selected. Used to trigger game effects like starting or updating quests.

Script commands follow specific naming conventions:
- `StartQuest_quest_id`: Begins a new quest
- `UpdateQuest_quest_id_stage_number`: Updates a quest to a specific stage

## Quest Objects

Quests represent objectives or storylines:

```json
{
  "id": "unique_quest_id",
  "title": "Quest Title",
  "description": "Overall description of the quest",
  "stages": [ ... array of stage objects ... ]
}
```

### id
A unique string identifier for the quest.

### title
The title of the quest as displayed in the quest log.

### description
A brief description of the quest's objective.

### stages
An array of stages that represent the progression of the quest.

## Quest Stage Objects

Each quest has multiple stages that track progress:

```json
{
  "id": 1,
  "description": "Short description for internal reference",
  "journal_entry": "Text that appears in the player's quest log"
}
```

### id
A numeric identifier for the stage, typically starting at 1 and incrementing.

### description
A short description used for development reference (not shown to the player).

### journal_entry
The text that appears in the player's quest log when they reach this stage.

## Best Practices

1. **Dialogue IDs**: Use descriptive names that indicate the content or purpose of the dialogue (e.g., "ai_escape_intro" rather than "dialogue1").

2. **Dialogue Flow**: Ensure that all `next_dialogue` values point to valid dialogue IDs or are explicitly set to `null`.

3. **Conversation Branches**: Design your dialogue tree to allow for meaningful branching based on player choices.

4. **Quest Integration**: Use script commands in responses to trigger quest updates at appropriate points in the conversation.

5. **Testing**: Thoroughly test all dialogue paths to ensure there are no dead ends or loops unless intentional.

6. **Validation**: Use the Dialogue Editor's validation feature to check for common errors before deploying.

By following this format, you can create rich, interactive narratives that players can explore through the Terminal Dialogue Simulator. The format is designed to be easily extended with additional fields as needed for more complex interactions.

