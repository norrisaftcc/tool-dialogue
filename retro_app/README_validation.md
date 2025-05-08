# Dialogue Validation Tool

This tool provides comprehensive validation for dialogue JSON files used in the Terminal Dialogue Simulator. It helps ensure consistent format, catches errors, and enforces best practices across all dialogue files.

## Features

- **Schema Validation**: Validates all dialogue files against the standardized JSON schema
- **Reference Checking**: Ensures all dialogue references point to valid destinations
- **Quest Verification**: Confirms quest references and stage progressions are valid
- **Circular Reference Detection**: Identifies loops in dialogue paths
- **Unreachable Content Check**: Finds dialogues that can't be accessed from the starting point
- **Naming Convention Validation**: Encourages consistent, descriptive IDs for dialogues, responses, and quests
- **Format Consistency**: Checks for standardized formatting like the ">" prefix for player responses
- **Missing Field Detection**: Identifies optional fields that should be present for consistency
- **Auto-fixing Capability**: Can automatically correct common issues and upgrade legacy format files
- **Batch Processing**: Can validate all JSON files in a directory at once
- **Detailed Reporting**: Provides clear, actionable feedback on issues found

## Usage

### Basic Validation

To validate a single dialogue file:

```bash
./dialogue_validator.py --file path/to/dialogue.json
```

### Comprehensive Checks 

To get detailed warnings including style issues:

```bash
./dialogue_validator.py --file path/to/dialogue.json --verbose
```

### Auto-fixing Issues

To attempt automatic fixes for common problems:

```bash
./dialogue_validator.py --file path/to/dialogue.json --fix
```

### Specify Output for Fixed Files

```bash
./dialogue_validator.py --file path/to/dialogue.json --fix --output-dir fixed_files/
```

### Batch Validation

To validate all JSON files in a directory:

```bash
./dialogue_validator.py --dir dialogue_files/ --pattern "*.json"
```

### Custom Schema

To use a different schema file:

```bash
./dialogue_validator.py --file path/to/dialogue.json --schema custom_schema.json
```

## Running the Test Suite

A test suite is included to demonstrate validation capabilities on various sample files:

```bash
cd tests
./run_validator_tests.py
```

This will run the validator against several test files designed to trigger different validation checks.

## Common Validation Issues

### Schema Errors

These indicate violations of the required structure:

- Missing required fields (e.g., missing `id` in a dialogue)
- Incorrect data types (e.g., using a number for a field that requires a string)
- Invalid values (e.g., using a negative number for XP rewards)

### Reference Errors

These affect dialogue flow and quest progression:

- References to non-existent dialogue IDs
- References to non-existent quests
- References to non-existent quest stages
- Unreachable dialogues that can't be accessed from the starting dialogue
- Circular references creating infinite loops

### Style Warnings

These recommend best practices:

- Non-descriptive dialogue IDs (e.g., "dialogue1" instead of "ai_escape_intro")
- Missing ">" prefix on player responses
- Inconsistent naming conventions
- Non-sequential quest stage IDs

## Upgrading Legacy Files

The tool can automatically upgrade older dialogue files to the latest format:

1. Run with the `--fix` option
2. The tool will add missing fields like `schema_version`, `metadata`, and `variables`
3. It will add `null` values for optional fields like `script`, `condition`, and `on_entry`
4. It will ensure proper structure for quest rewards and stages

## Integration with Workflow

Consider:

- Running validation before commits to ensure consistent formatting
- Adding validation to your editing workflow to catch issues early
- Using batch validation periodically to ensure all files remain compatible

## Further Reading

- See `README_dialogue_format.md` for the detailed dialogue format specification
- See `README_standardized_format.md` for naming conventions and best practices