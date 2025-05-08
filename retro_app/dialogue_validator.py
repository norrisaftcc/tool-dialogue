#!/usr/bin/env python
import json
import jsonschema
import os
import sys
import argparse
from pathlib import Path
from jsonschema import validate, ValidationError
from typing import Dict, List, Tuple, Any, Optional, Set
import glob
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger('dialogue_validator')

class DialogueValidator:
    """Comprehensive validator for dialogue JSON files"""
    
    def __init__(self, schema_path: str = "dialogue_schema.json", 
                 schema_version: str = "1.0"):
        """Initialize the validator with schema path and expected version"""
        self.schema_path = schema_path
        self.schema_version = schema_version
        self.schema = self._load_schema()
        self.statistics = {
            "files_checked": 0,
            "files_valid": 0,
            "files_invalid": 0,
            "errors_by_type": {},
            "warnings_by_type": {}
        }
        
    def _load_schema(self) -> Dict:
        """Load the JSON schema file"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Schema file '{self.schema_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schema file: {e}")
            sys.exit(1)
    
    def load_dialogue_file(self, file_path: str) -> Dict:
        """Load a dialogue JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Dialogue file '{file_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in dialogue file: {e}")
            sys.exit(1)
    
    def validate_schema(self, dialogue_data: Dict) -> Tuple[bool, Optional[ValidationError]]:
        """Validate dialogue data against the schema"""
        try:
            validate(instance=dialogue_data, schema=self.schema)
            return True, None
        except ValidationError as e:
            return False, e
    
    def check_dialogue_references(self, dialogue_data: Dict) -> Tuple[List[str], List[str]]:
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
        
        # Check for circular references and dead ends
        self._check_for_circular_references(dialogue_data, warnings)
        
        return errors, warnings
    
    def _check_for_circular_references(self, dialogue_data: Dict, warnings: List[str]) -> None:
        """Check for circular references and ensure proper conversation endings"""
        dialogue_dict = {d["id"]: d for d in dialogue_data["dialogues"]}
        
        # Track paths to detect cycles
        for dialogue_id in dialogue_dict:
            path = []
            self._dfs_check_cycles(dialogue_id, dialogue_dict, path, set(), warnings)
    
    def _dfs_check_cycles(self, dialogue_id: str, dialogue_dict: Dict, 
                         path: List[str], visited: Set[str], warnings: List[str]) -> None:
        """Depth-first search to check for dialogue cycles"""
        if dialogue_id in path:
            cycle = path[path.index(dialogue_id):] + [dialogue_id]
            warnings.append(f"Circular dialogue reference detected: {' -> '.join(cycle)}")
            return
        
        if dialogue_id in visited or dialogue_id is None:
            return
            
        visited.add(dialogue_id)
        path.append(dialogue_id)
        
        dialogue = dialogue_dict.get(dialogue_id)
        if dialogue:
            for response in dialogue["responses"]:
                next_id = response["next_dialogue"]
                if next_id:
                    self._dfs_check_cycles(next_id, dialogue_dict, path.copy(), visited, warnings)
        
        path.pop()
    
    def check_quest_references(self, dialogue_data: Dict) -> Tuple[List[str], List[str]]:
        """Check for valid quest references in dialogue scripts"""
        errors = []
        warnings = []
        
        # Check if quests exist
        if "quests" not in dialogue_data:
            return errors, warnings
            
        # Get all quest IDs
        quest_ids = {q["id"] for q in dialogue_data["quests"]}
        
        # Check script references to quests in dialogue entries
        for dialogue in dialogue_data["dialogues"]:
            # Check on_entry script if it exists
            if dialogue.get("on_entry") and dialogue["on_entry"] is not None:
                script = dialogue["on_entry"]
                self._check_script_quest_reference(script, quest_ids, dialogue["id"], None, errors)
            
            # Check response scripts
            for response in dialogue["responses"]:
                if response.get("script") and response["script"] is not None:
                    script = response["script"]
                    self._check_script_quest_reference(script, quest_ids, dialogue["id"], response["id"], errors)
            
        # Check for unused quests
        referenced_quest_ids = set()
        for dialogue in dialogue_data["dialogues"]:
            # Get references from on_entry
            if dialogue.get("on_entry") and dialogue["on_entry"] is not None:
                quest_id = self._extract_quest_id_from_script(dialogue["on_entry"])
                if quest_id:
                    referenced_quest_ids.add(quest_id)
            
            # Get references from response scripts
            for response in dialogue["responses"]:
                if response.get("script") and response["script"] is not None:
                    quest_id = self._extract_quest_id_from_script(response["script"])
                    if quest_id:
                        referenced_quest_ids.add(quest_id)
        
        unused_quests = quest_ids - referenced_quest_ids
        if unused_quests:
            for quest_id in unused_quests:
                warnings.append(f"Quest '{quest_id}' is defined but never referenced in any dialogue script")
                
        return errors, warnings
    
    def _check_script_quest_reference(self, script: str, quest_ids: Set[str], 
                                     dialogue_id: str, response_id: Optional[str], 
                                     errors: List[str]) -> None:
        """Check if a script command references a valid quest"""
        if script.startswith("StartQuest_") or script.startswith("UpdateQuest_") or script.startswith("CompleteQuest_"):
            parts = script.split("_")
            if len(parts) >= 2:
                quest_id = parts[1]
                if quest_id not in quest_ids:
                    if response_id:
                        errors.append(f"In dialogue '{dialogue_id}', response '{response_id}' script references non-existent quest '{quest_id}'")
                    else:
                        errors.append(f"In dialogue '{dialogue_id}', on_entry script references non-existent quest '{quest_id}'")
                
                # If it's an UpdateQuest command, check if the stage exists
                if script.startswith("UpdateQuest_") and len(parts) >= 3:
                    try:
                        stage_id = int(parts[2])
                        quest = next((q for q in dialogue_data["quests"] if q["id"] == quest_id), None)
                        if quest:
                            stage_ids = [s["id"] for s in quest["stages"]]
                            if stage_id not in stage_ids:
                                if response_id:
                                    errors.append(f"In dialogue '{dialogue_id}', response '{response_id}' script references non-existent stage {stage_id} for quest '{quest_id}'")
                                else:
                                    errors.append(f"In dialogue '{dialogue_id}', on_entry script references non-existent stage {stage_id} for quest '{quest_id}'")
                    except ValueError:
                        # Not a number, so can't be a valid stage reference
                        if response_id:
                            errors.append(f"In dialogue '{dialogue_id}', response '{response_id}' has invalid stage format in UpdateQuest command")
                        else:
                            errors.append(f"In dialogue '{dialogue_id}', on_entry has invalid stage format in UpdateQuest command")
    
    def _extract_quest_id_from_script(self, script: str) -> Optional[str]:
        """Extract quest ID from a script command if it exists"""
        if script and (script.startswith("StartQuest_") or 
                       script.startswith("UpdateQuest_") or 
                       script.startswith("CompleteQuest_")):
            parts = script.split("_")
            if len(parts) >= 2:
                return parts[1]
        return None
    
    def check_naming_conventions(self, dialogue_data: Dict) -> List[str]:
        """Check if dialogue and quest IDs follow naming conventions"""
        warnings = []
        
        # Check dialogue IDs
        for dialogue in dialogue_data["dialogues"]:
            if not self._is_valid_dialogue_id(dialogue["id"]):
                warnings.append(f"Dialogue ID '{dialogue['id']}' doesn't follow the recommended naming convention")
            
            # Check response IDs
            for response in dialogue["responses"]:
                if not self._is_valid_response_id(response["id"]):
                    warnings.append(f"Response ID '{response['id']}' in dialogue '{dialogue['id']}' doesn't follow the recommended naming convention")
        
        # Check quest IDs
        if "quests" in dialogue_data:
            for quest in dialogue_data["quests"]:
                if not self._is_valid_quest_id(quest["id"]):
                    warnings.append(f"Quest ID '{quest['id']}' doesn't follow the recommended naming convention")
        
        return warnings
    
    def _is_valid_dialogue_id(self, dialogue_id: str) -> bool:
        """Check if dialogue ID follows convention (e.g., character_purpose_state)"""
        # This is a simple check - dialogue IDs should contain underscores and be descriptive
        return "_" in dialogue_id and len(dialogue_id) > 5 and dialogue_id.islower()
    
    def _is_valid_response_id(self, response_id: str) -> bool:
        """Check if response ID follows convention (e.g., action_target)"""
        # Simple check for response IDs
        return "_" in response_id and len(response_id) > 3 and response_id.islower()
    
    def _is_valid_quest_id(self, quest_id: str) -> bool:
        """Check if quest ID follows naming convention"""
        # Simple check for quest IDs
        return "_" in quest_id or len(quest_id) > 3 and quest_id.islower()
    
    def check_player_response_format(self, dialogue_data: Dict) -> List[str]:
        """Check if player responses follow the '> ' prefix convention"""
        warnings = []
        
        for dialogue in dialogue_data["dialogues"]:
            for response in dialogue["responses"]:
                if not response["text"].startswith("> ") and not response["text"].startswith(">["):
                    warnings.append(f"Response '{response['id']}' in dialogue '{dialogue['id']}' doesn't start with '> ' prefix")
        
        return warnings
    
    def check_for_missing_fields(self, dialogue_data: Dict) -> List[str]:
        """Check for missing optional fields that should be present for consistency"""
        warnings = []
        
        # Check for schema_version
        if "schema_version" not in dialogue_data:
            warnings.append("Missing 'schema_version' field at the root level")
        
        # Check for metadata
        if "metadata" not in dialogue_data:
            warnings.append("Missing 'metadata' object at the root level")
        
        # Check for script fields in responses
        for dialogue in dialogue_data["dialogues"]:
            # Check for on_entry field
            if "on_entry" not in dialogue:
                warnings.append(f"Dialogue '{dialogue['id']}' is missing 'on_entry' field")
            
            # Check for script and condition fields in responses
            for response in dialogue["responses"]:
                if "script" not in response:
                    warnings.append(f"Response '{response['id']}' in dialogue '{dialogue['id']}' is missing 'script' field")
                if "condition" not in response:
                    warnings.append(f"Response '{response['id']}' in dialogue '{dialogue['id']}' is missing 'condition' field")
        
        # Check for variables section
        if "variables" not in dialogue_data:
            warnings.append("Missing 'variables' object at the root level")
        
        # Check for rewards in quests
        if "quests" in dialogue_data:
            for quest in dialogue_data["quests"]:
                if "rewards" not in quest:
                    warnings.append(f"Quest '{quest['id']}' is missing 'rewards' object")
                
                # Check for on_complete in stages
                for stage in quest["stages"]:
                    if "on_complete" not in stage:
                        warnings.append(f"Stage {stage['id']} in quest '{quest['id']}' is missing 'on_complete' field")
        
        # Check for characters section if image_url is used
        has_image_url = any("image_url" in dialogue for dialogue in dialogue_data["dialogues"])
        if has_image_url and "characters" not in dialogue_data:
            warnings.append("Dialogues use 'image_url' but there's no 'characters' section defined")
        
        return warnings
    
    def check_quest_progression(self, dialogue_data: Dict) -> List[str]:
        """Check if quest stages have sequential IDs starting from 1"""
        warnings = []
        
        if "quests" in dialogue_data:
            for quest in dialogue_data["quests"]:
                stage_ids = [stage["id"] for stage in quest["stages"]]
                expected_ids = list(range(1, len(stage_ids) + 1))
                
                if sorted(stage_ids) != expected_ids:
                    warnings.append(f"Quest '{quest['id']}' has non-sequential stage IDs: {stage_ids}. Expected: {expected_ids}")
        
        return warnings
    
    def validate_file(self, file_path: str) -> Tuple[bool, Dict]:
        """Validate a single dialogue file and return results"""
        logger.info(f"Validating file: {file_path}")
        result = {
            "path": file_path,
            "valid_schema": False,
            "schema_error": None,
            "reference_errors": [],
            "reference_warnings": [],
            "quest_errors": [],
            "quest_warnings": [],
            "naming_warnings": [],
            "response_format_warnings": [],
            "missing_field_warnings": [],
            "quest_progression_warnings": [],
            "all_errors": [],
            "all_warnings": []
        }
        
        # Load the dialogue file
        dialogue_data = self.load_dialogue_file(file_path)
        
        # Validate against schema
        is_valid, validation_error = self.validate_schema(dialogue_data)
        result["valid_schema"] = is_valid
        if not is_valid and validation_error:
            result["schema_error"] = str(validation_error)
            result["all_errors"].append(f"Schema error: {validation_error}")
        
        # Check dialogue references
        ref_errors, ref_warnings = self.check_dialogue_references(dialogue_data)
        result["reference_errors"] = ref_errors
        result["reference_warnings"] = ref_warnings
        result["all_errors"].extend(ref_errors)
        result["all_warnings"].extend(ref_warnings)
        
        # Check quest references
        quest_errors, quest_warnings = self.check_quest_references(dialogue_data)
        result["quest_errors"] = quest_errors
        result["quest_warnings"] = quest_warnings
        result["all_errors"].extend(quest_errors)
        result["all_warnings"].extend(quest_warnings)
        
        # Check naming conventions
        naming_warnings = self.check_naming_conventions(dialogue_data)
        result["naming_warnings"] = naming_warnings
        result["all_warnings"].extend(naming_warnings)
        
        # Check player response format
        format_warnings = self.check_player_response_format(dialogue_data)
        result["response_format_warnings"] = format_warnings
        result["all_warnings"].extend(format_warnings)
        
        # Check for missing fields
        missing_field_warnings = self.check_for_missing_fields(dialogue_data)
        result["missing_field_warnings"] = missing_field_warnings
        result["all_warnings"].extend(missing_field_warnings)
        
        # Check quest progression
        quest_progression_warnings = self.check_quest_progression(dialogue_data)
        result["quest_progression_warnings"] = quest_progression_warnings
        result["all_warnings"].extend(quest_progression_warnings)
        
        # Update statistics
        self.statistics["files_checked"] += 1
        if not result["all_errors"]:
            self.statistics["files_valid"] += 1
        else:
            self.statistics["files_invalid"] += 1
            
        # Track error types
        for error in result["all_errors"]:
            error_type = error.split(":")[0]
            self.statistics["errors_by_type"][error_type] = self.statistics["errors_by_type"].get(error_type, 0) + 1
            
        # Track warning types
        for warning in result["all_warnings"]:
            warning_type = warning.split(" ")[0]
            self.statistics["warnings_by_type"][warning_type] = self.statistics["warnings_by_type"].get(warning_type, 0) + 1
        
        return len(result["all_errors"]) == 0, result
    
    def validate_directory(self, directory_path: str, pattern: str = "*.json") -> List[Dict]:
        """Validate all JSON files in a directory"""
        results = []
        
        # Find all JSON files in the directory
        file_paths = glob.glob(os.path.join(directory_path, pattern))
        
        if not file_paths:
            logger.warning(f"No files matching pattern '{pattern}' found in '{directory_path}'")
            return results
        
        logger.info(f"Found {len(file_paths)} files to validate")
        
        # Validate each file
        for file_path in file_paths:
            _, result = self.validate_file(file_path)
            results.append(result)
        
        return results
    
    def print_validation_results(self, results: List[Dict], verbose: bool = False) -> None:
        """Print validation results in a readable format"""
        valid_count = sum(1 for r in results if not r["all_errors"])
        total_count = len(results)
        
        logger.info(f"\n===== VALIDATION SUMMARY =====")
        logger.info(f"Files checked: {total_count}")
        logger.info(f"Files valid: {valid_count} ({(valid_count/total_count)*100:.1f}%)")
        logger.info(f"Files with errors: {total_count - valid_count} ({((total_count-valid_count)/total_count)*100:.1f}%)")
        
        # Print details for each file
        for result in results:
            if result["all_errors"]:
                logger.error(f"\n❌ File: {result['path']}")
                for error in result["all_errors"]:
                    logger.error(f"   - {error}")
            else:
                logger.info(f"\n✅ File: {result['path']}")
            
            if verbose and result["all_warnings"]:
                logger.warning(f"   Warnings:")
                for warning in result["all_warnings"]:
                    logger.warning(f"   - {warning}")
        
        # Print statistics
        logger.info(f"\n===== ERROR STATISTICS =====")
        for error_type, count in sorted(self.statistics["errors_by_type"].items(), key=lambda x: x[1], reverse=True):
            logger.info(f"{error_type}: {count}")
            
        if verbose:
            logger.info(f"\n===== WARNING STATISTICS =====")
            for warning_type, count in sorted(self.statistics["warnings_by_type"].items(), key=lambda x: x[1], reverse=True):
                logger.info(f"{warning_type}: {count}")
    
    def suggest_fixes(self, dialogue_data: Dict) -> List[str]:
        """Suggest fixes for common issues"""
        suggestions = []
        
        # Add schema_version if missing
        if "schema_version" not in dialogue_data:
            suggestions.append(f"Add schema_version: \"{self.schema_version}\"")
        
        # Add metadata if missing
        if "metadata" not in dialogue_data:
            suggestions.append("Add a metadata object with title, author, creation_date, and description")
        
        # Check for null script fields
        for dialogue in dialogue_data["dialogues"]:
            for response in dialogue["responses"]:
                if "script" not in response:
                    suggestions.append(f"Add \"script\": null to response {response['id']} in dialogue {dialogue['id']}")
                if "condition" not in response:
                    suggestions.append(f"Add \"condition\": null to response {response['id']} in dialogue {dialogue['id']}")
        
        # Check for missing on_entry fields
        for dialogue in dialogue_data["dialogues"]:
            if "on_entry" not in dialogue:
                suggestions.append(f"Add \"on_entry\": null to dialogue {dialogue['id']}")
        
        # Check for variables section
        if "variables" not in dialogue_data:
            suggestions.append("Add a variables object to track global state (can be empty: {})")
        
        # Check quest reward structures
        if "quests" in dialogue_data:
            for quest in dialogue_data["quests"]:
                if "rewards" not in quest:
                    suggestions.append(f"Add a rewards object to quest {quest['id']}")
                
                # Check for on_complete in stages
                for stage in quest["stages"]:
                    if "on_complete" not in stage:
                        suggestions.append(f"Add \"on_complete\": null to stage {stage['id']} in quest {quest['id']}")
        
        return suggestions
    
    def upgrade_dialogue_file(self, dialogue_data: Dict) -> Dict:
        """Attempt to automatically upgrade a dialogue file to match the schema"""
        # Create a copy to modify
        upgraded = dialogue_data.copy()
        
        # Add schema_version if missing
        if "schema_version" not in upgraded:
            upgraded["schema_version"] = self.schema_version
        
        # Add metadata if missing
        if "metadata" not in upgraded:
            upgraded["metadata"] = {
                "title": "Auto-upgraded Dialogue",
                "author": "Dialogue Validator",
                "creation_date": "2025-05-08",
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
        if "quests" in upgraded:
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
    parser = argparse.ArgumentParser(description='Validate dialogue JSON files against schema and best practices')
    parser.add_argument('--file', help='Specific dialogue JSON file to validate')
    parser.add_argument('--dir', help='Directory containing JSON files to validate')
    parser.add_argument('--pattern', default='*.json', help='File pattern for validation (default: *.json)')
    parser.add_argument('--schema', default='dialogue_schema.json', help='Path to the schema file (default: dialogue_schema.json)')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix issues automatically')
    parser.add_argument('--output-dir', help='Output directory for fixed versions (only used with --fix)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed warning information')
    parser.add_argument('--quiet', '-q', action='store_true', help='Show only summary information')
    
    args = parser.parse_args()
    
    # Adjust logging level based on verbosity
    if args.quiet:
        logger.setLevel(logging.WARNING)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Create validator
    validator = DialogueValidator(schema_path=args.schema)
    
    # Validate files
    results = []
    
    if args.file:
        # Validate a single file
        is_valid, result = validator.validate_file(args.file)
        results = [result]
        
        # Fix if requested
        if args.fix:
            dialogue_data = validator.load_dialogue_file(args.file)
            suggestions = validator.suggest_fixes(dialogue_data)
            
            if suggestions:
                logger.info("\n💡 Suggested fixes:")
                for suggestion in suggestions:
                    logger.info(f"   - {suggestion}")
                
                logger.info("\n🔧 Attempting automatic fixes...")
                fixed_data = validator.upgrade_dialogue_file(dialogue_data)
                
                # Validate the fixed data
                fixed_valid, _ = validator.validate_schema(fixed_data)
                
                if fixed_valid:
                    logger.info("✅ Automatic fixes were successful!")
                    
                    # Save fixed data
                    if args.output_dir:
                        os.makedirs(args.output_dir, exist_ok=True)
                        file_name = os.path.basename(args.file)
                        output_path = os.path.join(args.output_dir, file_name)
                    else:
                        file_path = Path(args.file)
                        output_path = file_path.with_stem(file_path.stem + "_fixed")
                    
                    with open(output_path, 'w') as f:
                        json.dump(fixed_data, f, indent=2)
                    logger.info(f"✍️  Fixed data written to {output_path}")
                else:
                    logger.error("❌ Automatic fixes were not sufficient to make the file valid")
        
    elif args.dir:
        # Validate all files in a directory
        results = validator.validate_directory(args.dir, args.pattern)
        
        # Fix if requested
        if args.fix and args.output_dir:
            logger.info("\n🔧 Attempting automatic fixes for all invalid files...")
            os.makedirs(args.output_dir, exist_ok=True)
            
            fix_count = 0
            for result in results:
                if result["all_errors"]:
                    file_path = result["path"]
                    dialogue_data = validator.load_dialogue_file(file_path)
                    fixed_data = validator.upgrade_dialogue_file(dialogue_data)
                    
                    # Validate the fixed data
                    fixed_valid, _ = validator.validate_schema(fixed_data)
                    
                    if fixed_valid:
                        # Save fixed data
                        file_name = os.path.basename(file_path)
                        output_path = os.path.join(args.output_dir, file_name)
                        
                        with open(output_path, 'w') as f:
                            json.dump(fixed_data, f, indent=2)
                        logger.info(f"✅ Fixed and saved: {output_path}")
                        fix_count += 1
                    else:
                        logger.warning(f"⚠️  Could not fully fix: {file_path}")
            
            logger.info(f"\nSuccessfully fixed {fix_count} out of {len(results)} files")
    else:
        logger.error("Error: Must specify either --file or --dir")
        parser.print_help()
        return 1
    
    # Print validation results
    validator.print_validation_results(results, args.verbose)
    
    # Return appropriate exit code
    if all(not r["all_errors"] for r in results):
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())