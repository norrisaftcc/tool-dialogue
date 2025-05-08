import json
import jsonschema
import argparse
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    """Load the JSON schema file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file '{schema_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema file: {e}")
        sys.exit(1)

def load_dialogue_file(file_path):
    """Load a dialogue JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Dialogue file '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in dialogue file: {e}")
        sys.exit(1)

def validate_dialogue(dialogue_data, schema):
    """Validate dialogue data against the schema"""
    try:
        validate(instance=dialogue_data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e

def check_dialogue_references(dialogue_data):
    """Check for missing or circular dialogue references"""
    errors = []
    warnings = []
    
    # Get all dialogue IDs
    dialogue_ids = {d["id"] for d in dialogue_data["dialogues"]}
    
    # Check starting dialogue
    if dialogue_data["starting_dialogue"] not in dialogue_ids:
        errors.append(f"Starting dialogue '{dialogue_data['starting_dialogue']}' doesn't exist in dialogues array")
    
    # Check next_dialogue references
    for dialogue in dialogue_data["dialogues"]:
        for response in dialogue["responses"]:
            next_id = response["next_dialogue"]
            if next_id is not None and next_id not in dialogue_ids:
                errors.append(f"In dialogue '{dialogue['id']}', response '{response['id']}' references non-existent dialogue '{next_id}'")
    
    # Check for dialogues that can't be reached from starting point
    reachable = set()
    to_check = [dialogue_data["starting_dialogue"]]
    
    while to_check:
        current = to_check.pop()
        if current in reachable or current is None:
            continue
            
        reachable.add(current)
        
        # Find dialogue object
        dialogue = next((d for d in dialogue_data["dialogues"] if d["id"] == current), None)
        if dialogue:
            # Add all next_dialogue values to check
            for response in dialogue["responses"]:
                if response["next_dialogue"] and response["next_dialogue"] not in reachable:
                    to_check.append(response["next_dialogue"])
    
    unreachable = dialogue_ids - reachable
    if unreachable:
        for d_id in unreachable:
            warnings.append(f"Dialogue '{d_id}' is unreachable from the starting dialogue")
    
    # Check script references to quests
    quest_ids = {q["id"] for q in dialogue_data["quests"]}
    
    for dialogue in dialogue_data["dialogues"]:
        # Check on_entry script if it exists
        if dialogue.get("on_entry") and dialogue["on_entry"] is not None:
            script = dialogue["on_entry"]
            if script.startswith("StartQuest_") or script.startswith("UpdateQuest_") or script.startswith("CompleteQuest_"):
                quest_id = script.split("_")[1]
                if quest_id not in quest_ids:
                    errors.append(f"In dialogue '{dialogue['id']}', on_entry script references non-existent quest '{quest_id}'")
        
        # Check response scripts
        for response in dialogue["responses"]:
            if response.get("script") and response["script"] is not None:
                script = response["script"]
                if script.startswith("StartQuest_") or script.startswith("CompleteQuest_"):
                    quest_id = script.split("_")[1]
                    if quest_id not in quest_ids:
                        errors.append(f"In dialogue '{dialogue['id']}', response '{response['id']}' script references non-existent quest '{quest_id}'")
                elif script.startswith("UpdateQuest_"):
                    parts = script.split("_")
                    if len(parts) >= 2:
                        quest_id = parts[1]
                        if quest_id not in quest_ids:
                            errors.append(f"In dialogue '{dialogue['id']}', response '{response['id']}' script references non-existent quest '{quest_id}'")
                        
                        # Check if quest stage exists
                        if len(parts) >= 3:
                            try:
                                stage_id = int(parts[2])
                                quest = next((q for q in dialogue_data["quests"] if q["id"] == quest_id), None)
                                if quest:
                                    stage_ids = [s["id"] for s in quest["stages"]]
                                    if stage_id not in stage_ids:
                                        errors.append(f"In dialogue '{dialogue['id']}', response '{response['id']}' script references non-existent stage {stage_id} for quest '{quest_id}'")
                            except ValueError:
                                # Not a number, so can't be a valid stage reference
                                errors.append(f"In dialogue '{dialogue['id']}', response '{response['id']}' has invalid stage format in UpdateQuest command")
    
    return errors, warnings

def suggest_fixes(dialogue_data, schema_version="1.0"):
    """Suggest fixes to make the dialogue file conform to the schema"""
    suggestions = []
    
    # Add schema_version if missing
    if "schema_version" not in dialogue_data:
        suggestions.append(f"Add schema_version: \"{schema_version}\"")
    
    # Add metadata if missing
    if "metadata" not in dialogue_data:
        suggestions.append("Add a metadata object with title, author, creation_date, and description")
    
    # Check for null script fields
    for dialogue in dialogue_data["dialogues"]:
        for response in dialogue["responses"]:
            if "script" not in response:
                suggestions.append(f"Add \"script\": null to response {response['id']} in dialogue {dialogue['id']}")
    
    # Check for missing on_entry fields
    for dialogue in dialogue_data["dialogues"]:
        if "on_entry" not in dialogue:
            suggestions.append(f"Add \"on_entry\": null to dialogue {dialogue['id']}")
    
    # Check for empty response arrays
    for dialogue in dialogue_data["dialogues"]:
        if len(dialogue["responses"]) == 0:
            suggestions.append(f"Add at least one response with next_dialogue: null to dialogue {dialogue['id']}")
    
    # Check for variables section
    if "variables" not in dialogue_data:
        suggestions.append("Add a variables object to track global state (can be empty: {})")
    
    # Check quest reward structures
    for quest in dialogue_data["quests"]:
        if "rewards" not in quest:
            suggestions.append(f"Add a rewards object to quest {quest['id']}")
    
    return suggestions

def upgrade_dialogue_file(dialogue_data, schema_version="1.0"):
    """Attempt to automatically upgrade a dialogue file to match the schema"""
    # Create a copy to modify
    upgraded = dialogue_data.copy()
    
    # Add schema_version if missing
    if "schema_version" not in upgraded:
        upgraded["schema_version"] = schema_version
    
    # Add metadata if missing
    if "metadata" not in upgraded:
        upgraded["metadata"] = {
            "title": "Auto-upgraded Dialogue",
            "author": "Schema Validator",
            "creation_date": "2025-05-07",
            "description": "Automatically upgraded from legacy format"
        }
    
    # Add missing script fields and on_entry fields
    for dialogue in upgraded["dialogues"]:
        if "on_entry" not in dialogue:
            dialogue["on_entry"] = None
            
        for response in dialogue["responses"]:
            if "script" not in response:
                response["script"] = None
            if "condition" not in response:
                response["condition"] = None
    
    # Handle empty response arrays
    for dialogue in upgraded["dialogues"]:
        if len(dialogue["responses"]) == 0:
            dialogue["responses"] = [{
                "id": f"end_{dialogue['id']}",
                "text": "> [End Conversation]",
                "next_dialogue": None,
                "script": None,
                "condition": None
            }]
    
    # Add variables section if missing
    if "variables" not in upgraded:
        upgraded["variables"] = {}
    
    # Add quest rewards structure if missing
    for quest in upgraded["quests"]:
        if "rewards" not in quest:
            quest["rewards"] = {
                "xp": 0,
                "items": []
            }
        # Add on_complete to stages if missing
        for stage in quest["stages"]:
            if "on_complete" not in stage:
                stage["on_complete"] = None
    
    return upgraded

def main():
    parser = argparse.ArgumentParser(description='Validate dialogue JSON files against the schema')
    parser.add_argument('file', help='The dialogue JSON file to validate')
    parser.add_argument('--schema', default='dialogue_schema.json', help='Path to the schema file (default: dialogue_schema.json)')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix issues automatically')
    parser.add_argument('--output', help='Output file for fixed version (only used with --fix)')
    
    args = parser.parse_args()
    
    # Load schema
    schema = load_schema(args.schema)
    
    # Load dialogue file
    dialogue_data = load_dialogue_file(args.file)
    
    # Validate against schema
    is_valid, validation_error = validate_dialogue(dialogue_data, schema)
    
    if is_valid:
        print(f"✅ File '{args.file}' is valid according to the schema")
    else:
        print(f"❌ File '{args.file}' is invalid:")
        print(f"   {validation_error.message}")
        print(f"   Path: {' → '.join(str(p) for p in validation_error.path)}")
    
    # Check dialogue references
    errors, warnings = check_dialogue_references(dialogue_data)
    
    if errors:
        print("\n⚠️ Reference errors found:")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print("\n⚠️ Reference warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not is_valid or errors:
        suggestions = suggest_fixes(dialogue_data)
        print("\n💡 Suggested fixes:")
        for suggestion in suggestions:
            print(f"   - {suggestion}")
        
        if args.fix:
            print("\n🔧 Attempting automatic fixes...")
            fixed_data = upgrade_dialogue_file(dialogue_data)
            
            # Validate the fixed data
            fixed_valid, fixed_error = validate_dialogue(fixed_data, schema)
            
            if fixed_valid:
                print("✅ Automatic fixes were successful!")
                
                # Save fixed data if output file specified
                if args.output:
                    output_path = args.output
                else:
                    file_path = Path(args.file)
                    output_path = file_path.with_stem(file_path.stem + "_fixed")
                
                with open(output_path, 'w') as f:
                    json.dump(fixed_data, f, indent=2)
                print(f"✍️  Fixed data written to {output_path}")
            else:
                print("❌ Automatic fixes were not sufficient to make the file valid")
                print(f"   Remaining error: {fixed_error.message}")
    
    # Return appropriate exit code
    if not is_valid or errors:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())